"""Distingue resultado RECIBIDO, VALIDADO y ACEPTADO (README §5.2).

Solo el Cognitive Core acepta. La firma/validez estructural prueba procedencia y forma,
no corrección semántica.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class ResultState(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True)
class ModelResult:
    task_id: str
    node_id: str
    model_id: str
    raw_text: str
    state: ResultState = ResultState.RECEIVED
    checks: tuple[str, ...] = ()
    rejection_reason: str | None = None

    def validated(self, checks: tuple[str, ...]) -> ModelResult:
        if self.state is not ResultState.RECEIVED or not checks:
            raise ValueError("solo un resultado RECEIVED con al menos una comprobación")
        return replace(self, state=ResultState.VALIDATED, checks=checks)

    def accepted(self) -> ModelResult:
        if self.state is not ResultState.VALIDATED:
            raise ValueError("solo se acepta un resultado VALIDATED")
        return replace(self, state=ResultState.ACCEPTED)

    def rejected(self, reason: str) -> ModelResult:
        return replace(self, state=ResultState.REJECTED, rejection_reason=reason)
