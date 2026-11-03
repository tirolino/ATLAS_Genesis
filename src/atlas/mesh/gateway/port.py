from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class InferenceRequest:
    model_id: str
    messages: tuple[dict[str, str], ...]
    json_schema: dict[str, Any] | None = None  # salida estructurada obligatoria si se indica
    max_tokens: int = 1024
    temperature: float = 0.0
    timeout_s: float = 60.0


@dataclass(frozen=True)
class InferenceResult:
    model_id: str
    node_id: str
    raw_text: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: int
    engine: str


class InferencePort(Protocol):
    """Contrato que el resto de ATLAS conoce. Cada motor lo implementa en un adaptador."""

    def generate(self, request: InferenceRequest) -> InferenceResult: ...
