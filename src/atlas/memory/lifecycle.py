"""Ciclo de vida de una memoria candidata.

RECEIVED -> QUARANTINED -> VALIDATED -> ACCEPTED   (REJECTED desde cualquier estado previo)
                                          ACCEPTED -> REVOKED

Reglas deterministas (no dependen de ningún LLM):
- Ningún actor LLM puede validar ni aceptar.
- Si la fuente es T0/T1, aceptar exige un HUMANO, o un validador DETERMINISTA con evidencia.
- Toda transición lleva motivo y queda en el historial (para auditoría y rollback).
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum

from atlas.guardian.policy import PolicyViolation, TrustTier


class MemoryStatus(str, Enum):
    RECEIVED = "received"
    QUARANTINED = "quarantined"
    VALIDATED = "validated"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REVOKED = "revoked"


class MemoryKind(str, Enum):
    FACT = "fact"
    HYPOTHESIS = "hypothesis"
    MODEL_OUTPUT = "model_output"
    EXPERIENCE = "experience"


class ActorKind(str, Enum):
    DETERMINISTIC_VALIDATOR = "deterministic_validator"
    HUMAN = "human"
    COGNITIVE_CORE = "cognitive_core"
    LLM = "llm"


class InvalidTransition(PolicyViolation):
    pass


_ALLOWED: dict[MemoryStatus, frozenset[MemoryStatus]] = {
    MemoryStatus.RECEIVED: frozenset({MemoryStatus.QUARANTINED, MemoryStatus.REJECTED}),
    MemoryStatus.QUARANTINED: frozenset({MemoryStatus.VALIDATED, MemoryStatus.REJECTED}),
    MemoryStatus.VALIDATED: frozenset({MemoryStatus.ACCEPTED, MemoryStatus.REJECTED}),
    MemoryStatus.ACCEPTED: frozenset({MemoryStatus.REVOKED}),
    MemoryStatus.REJECTED: frozenset(),
    MemoryStatus.REVOKED: frozenset(),
}


@dataclass(frozen=True)
class Transition:
    from_status: MemoryStatus
    to_status: MemoryStatus
    actor_kind: ActorKind
    actor_id: str
    reason: str
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class MemoryCandidate:
    memory_id: str
    content: str
    kind: MemoryKind
    source_ref: str
    source_trust: TrustTier
    status: MemoryStatus = MemoryStatus.RECEIVED
    history: tuple[Transition, ...] = field(default=())


def transition(
    candidate: MemoryCandidate,
    to: MemoryStatus,
    *,
    actor_kind: ActorKind,
    actor_id: str,
    reason: str,
    evidence_refs: tuple[str, ...] = (),
) -> MemoryCandidate:
    if to not in _ALLOWED[candidate.status]:
        raise InvalidTransition(f"{candidate.status.value} -> {to.value} no permitido")
    if not reason.strip():
        raise InvalidTransition("toda transición requiere un motivo")
    if to in (MemoryStatus.VALIDATED, MemoryStatus.ACCEPTED) and actor_kind is ActorKind.LLM:
        raise InvalidTransition("un LLM no puede validar ni aceptar memoria")
    if to is MemoryStatus.ACCEPTED and candidate.source_trust < TrustTier.T2:
        human = actor_kind is ActorKind.HUMAN
        verified = actor_kind is ActorKind.DETERMINISTIC_VALIDATOR and bool(evidence_refs)
        if not (human or verified):
            raise InvalidTransition(
                "fuente T0/T1: aceptar exige humano o validador determinista con evidencia"
            )
    step = Transition(candidate.status, to, actor_kind, actor_id, reason, evidence_refs)
    return replace(candidate, status=to, history=(*candidate.history, step))
