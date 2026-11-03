"""Adaptador para la API HTTP local de Ollama.

Usa salida estructurada (`format` = JSON Schema). Aun así el resultado se trata como
NO CONFIABLE: se valida de nuevo en el Cognitive Core (ADR-0003).
"""

from __future__ import annotations

import time

import httpx

from atlas.mesh.gateway.port import (
    InferenceError,
    InferenceRequest,
    InferenceResult,
    InferenceUnavailable,
)


class OllamaAdapter:
    """Adaptador síncrono a la API local de chat de Ollama."""

    def __init__(self, base_url: str, node_id: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._node_id = node_id

    def generate(self, request: InferenceRequest) -> InferenceResult:
        if request.timeout_s <= 0:
            raise ValueError("timeout_s debe ser mayor que cero")
        payload: dict[str, object] = {
            "model": request.model_id,
            "messages": list(request.messages),
            "stream": False,
            "options": {"temperature": request.temperature, "num_predict": request.max_tokens},
        }
        if request.json_schema is not None:
            payload["format"] = request.json_schema
        started = time.monotonic()
        try:
            resp = httpx.post(
                f"{self._base_url}/api/chat", json=payload, timeout=request.timeout_s
            )
        except httpx.TransportError as exc:
            raise InferenceUnavailable("Ollama no está disponible") from exc
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise InferenceError(f"Ollama respondió HTTP {exc.response.status_code}") from exc
        try:
            data = resp.json()
        except ValueError as exc:
            raise InferenceError("Ollama devolvió una respuesta JSON inválida") from exc

        content, prompt_tokens, completion_tokens = _parse_response(data)
        return InferenceResult(
            model_id=request.model_id,
            node_id=self._node_id,
            raw_text=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_ms=int((time.monotonic() - started) * 1000),
            engine="ollama",
        )


def _parse_response(data: object) -> tuple[str, int, int]:
    if not isinstance(data, dict):
        raise InferenceError("Ollama devolvió una respuesta con formato inválido")
    message = data.get("message")
    if not isinstance(message, dict):
        raise InferenceError("Ollama omitió el mensaje de respuesta")
    content = message.get("content")
    if not isinstance(content, str):
        raise InferenceError("Ollama devolvió contenido de respuesta inválido")
    prompt_tokens = _token_count(data.get("prompt_eval_count", 0), "prompt_eval_count")
    completion_tokens = _token_count(data.get("eval_count", 0), "eval_count")
    return content, prompt_tokens, completion_tokens


def _token_count(value: object, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise InferenceError(f"Ollama devolvió {field} inválido")
    return value
