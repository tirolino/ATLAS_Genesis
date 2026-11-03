"""Adaptador Ollama (API HTTP local). Sin tests unitarios: requiere un servidor Ollama.

Usa salida estructurada (`format` = JSON Schema). Aun así el resultado se trata como
NO CONFIABLE: se valida de nuevo en el Cognitive Core (ADR-0003).
"""

from __future__ import annotations

import time

import httpx

from atlas.mesh.gateway.port import InferenceRequest, InferenceResult


class OllamaAdapter:
    def __init__(self, base_url: str, node_id: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._node_id = node_id

    def generate(self, request: InferenceRequest) -> InferenceResult:
        payload: dict[str, object] = {
            "model": request.model_id,
            "messages": list(request.messages),
            "stream": False,
            "options": {"temperature": request.temperature, "num_predict": request.max_tokens},
        }
        if request.json_schema is not None:
            payload["format"] = request.json_schema
        started = time.monotonic()
        resp = httpx.post(f"{self._base_url}/api/chat", json=payload, timeout=request.timeout_s)
        resp.raise_for_status()
        data = resp.json()
        return InferenceResult(
            model_id=request.model_id,
            node_id=self._node_id,
            raw_text=data["message"]["content"],
            prompt_tokens=int(data.get("prompt_eval_count", 0)),
            completion_tokens=int(data.get("eval_count", 0)),
            latency_ms=int((time.monotonic() - started) * 1000),
            engine="ollama",
        )
