-- PostgreSQL = fuente de verdad (ADR-0007). Los embeddings son DERIVADOS y reconstruibles.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE atlas_identity (
    atlas_id        text PRIMARY KEY,
    public_key_hex  text NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE identity_versions (
    atlas_id             text NOT NULL REFERENCES atlas_identity(atlas_id),
    version              integer NOT NULL,
    constitution_hash    text NOT NULL,
    previous_version_hash text,
    signature            text NOT NULL,
    created_at           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (atlas_id, version)
);

-- Log de auditoría encadenado y firmado; append-only a nivel de base de datos.
CREATE TABLE audit_log (
    seq            bigint PRIMARY KEY,
    ts             timestamptz NOT NULL,
    event_type     text NOT NULL,
    payload        jsonb NOT NULL,
    prev_hash      text NOT NULL,
    signer_key_id  text NOT NULL,
    entry_hash     text NOT NULL UNIQUE,
    signature      text NOT NULL
);
CREATE FUNCTION audit_log_immutable() RETURNS trigger AS $$
BEGIN RAISE EXCEPTION 'audit_log es append-only'; END $$ LANGUAGE plpgsql;
CREATE TRIGGER audit_log_no_update BEFORE UPDATE OR DELETE ON audit_log
    FOR EACH ROW EXECUTE FUNCTION audit_log_immutable();

CREATE TABLE memories (
    memory_id    uuid PRIMARY KEY,
    kind         text NOT NULL CHECK (kind IN ('fact','hypothesis','model_output','experience')),
    status       text NOT NULL CHECK (status IN
                   ('received','quarantined','validated','accepted','rejected','revoked')),
    content      text NOT NULL,
    source_ref   text NOT NULL,
    source_trust smallint NOT NULL CHECK (source_trust BETWEEN 0 AND 3),
    created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE memory_transitions (
    id            bigserial PRIMARY KEY,
    memory_id     uuid NOT NULL REFERENCES memories(memory_id),
    from_status   text NOT NULL,
    to_status     text NOT NULL,
    actor_kind    text NOT NULL,
    actor_id      text NOT NULL,
    reason        text NOT NULL CHECK (length(trim(reason)) > 0),
    evidence_refs text[] NOT NULL DEFAULT '{}',
    created_at    timestamptz NOT NULL DEFAULT now()
);
-- Solo memorias ACCEPTED se indexan. Ajusta la dimensión al modelo de embeddings elegido.
CREATE TABLE memory_embeddings (
    memory_id uuid PRIMARY KEY REFERENCES memories(memory_id),
    embedding vector(768) NOT NULL
);

CREATE TABLE checkpoints (
    manifest_hash text PRIMARY KEY,
    manifest      jsonb NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE mesh_nodes (
    node_id         text PRIMARY KEY,
    public_key_hex  text NOT NULL,
    trust_tier      smallint NOT NULL DEFAULT 0 CHECK (trust_tier BETWEEN 0 AND 3),
    declared_hw     jsonb NOT NULL,       -- DECLARADO por el agente, no verificado
    last_heartbeat  timestamptz,
    revoked_at      timestamptz
);
CREATE TABLE mesh_models (
    model_id        text PRIMARY KEY,
    spec            jsonb NOT NULL,
    artifact_sha256 text NOT NULL,
    approved        boolean NOT NULL DEFAULT false,
    eval_score      numeric
);
CREATE TABLE mesh_node_models (
    node_id  text REFERENCES mesh_nodes(node_id),
    model_id text REFERENCES mesh_models(model_id),
    PRIMARY KEY (node_id, model_id)
);
CREATE TABLE mesh_tasks (
    task_id        uuid PRIMARY KEY,
    task_type      text NOT NULL,
    data_class     smallint NOT NULL CHECK (data_class BETWEEN 0 AND 3),
    strategy       text NOT NULL,
    status         text NOT NULL,
    input_sha256   text NOT NULL,         -- hash, no el contenido
    created_at     timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE mesh_task_assignments (
    assignment_id uuid PRIMARY KEY,
    task_id       uuid NOT NULL REFERENCES mesh_tasks(task_id),
    node_id       text NOT NULL REFERENCES mesh_nodes(node_id),
    model_id      text NOT NULL REFERENCES mesh_models(model_id),
    status        text NOT NULL,
    UNIQUE (task_id, node_id, model_id)   -- idempotencia de asignación
);
CREATE TABLE mesh_results (
    result_id     uuid PRIMARY KEY,
    assignment_id uuid NOT NULL REFERENCES mesh_task_assignments(assignment_id),
    state         text NOT NULL CHECK (state IN ('received','validated','accepted','rejected')),
    output_sha256 text NOT NULL,
    checks        text[] NOT NULL DEFAULT '{}'
);
