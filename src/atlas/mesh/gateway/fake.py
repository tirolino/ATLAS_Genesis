"""Motor de inferencia falso y determinista para tests y desarrollo sin GPU."""

from __future__ import annotations

from atlas.mesh.gateway.port import InferenceRequest, InferenceResult


class FakeInference:
    def __init__(self, node_id: str, scripted: list[str]) -> None:
        self._node_id = node_id
        self._scripted = list(scripted)
        self.calls: list[InferenceRequest] = []

    def generate(self, request: InferenceRequest) -> InferenceResult:
        self.calls.append(request)
        text = self._scripted.pop(0)
        return InferenceResult(
            model_id=request.model_id, node_id=self._node_id, raw_text=text,
            prompt_tokens=10, completion_tokens=len(text) // 4, latency_ms=5, engine="fake",
        )
