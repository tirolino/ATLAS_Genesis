"""Modelo de identidad. DID (did:key / did:web) queda para ADR posterior (ver ADR-0006).

`constitution_hash` ancla el conjunto de reglas nucleares (documento firmado) que se inyecta
en el contexto de cualquier LLM. Cambiar de modelo NO cambia la identidad; cambiar la
constitución sí, y exige una nueva versión firmada y auditada.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AtlasIdentity:
    atlas_id: str
    public_key_hex: str
    version: int
    constitution_hash: str  # "sha256:..."
    created_at: str
    previous_version_hash: str | None = None
