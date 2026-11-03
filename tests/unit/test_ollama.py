import httpx
import pytest

from atlas.mesh.gateway.ollama import OllamaAdapter
from atlas.mesh.gateway.port import InferenceError, InferenceRequest, InferenceUnavailable


def _request(
    *,
    timeout_s: float = 2.5,
    json_schema: dict[str, object] | None = None,
) -> InferenceRequest:
    return InferenceRequest(
        model_id="local-model",
        messages=({"role": "user", "content": "hello"},),
        timeout_s=timeout_s,
        json_schema=json_schema,
    )


def test_ollama_adapter_sends_request_and_parses_response(monkeypatch: pytest.MonkeyPatch):
    call: dict[str, object] = {}

    def post(url: str, *, json: object, timeout: float) -> httpx.Response:
        call.update(url=url, json=json, timeout=timeout)
        return httpx.Response(
            200,
            json={
                "message": {"content": '{"ok": true}'},
                "prompt_eval_count": 12,
                "eval_count": 4,
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", post)
    request = _request(json_schema={"type": "object"})

    result = OllamaAdapter("http://127.0.0.1:11434/", "node-1").generate(request)

    assert call["url"] == "http://127.0.0.1:11434/api/chat"
    assert call["timeout"] == 2.5
    assert call["json"] == {
        "model": "local-model",
        "messages": [{"role": "user", "content": "hello"}],
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 1024},
        "format": {"type": "object"},
    }
    assert result.raw_text == '{"ok": true}'
    assert result.prompt_tokens == 12
    assert result.completion_tokens == 4
    assert result.node_id == "node-1"
    assert result.engine == "ollama"


@pytest.mark.parametrize("error", [httpx.ConnectTimeout("timeout"), httpx.ConnectError("offline")])
def test_ollama_adapter_reports_unavailability(
    monkeypatch: pytest.MonkeyPatch, error: httpx.TransportError
):
    def post(url: str, *, json: object, timeout: float) -> httpx.Response:
        raise error

    monkeypatch.setattr(httpx, "post", post)

    with pytest.raises(InferenceUnavailable) as exc_info:
        OllamaAdapter("http://127.0.0.1:11434", "node-1").generate(_request())

    assert exc_info.value.__cause__ is error


def test_ollama_adapter_reports_http_errors(monkeypatch: pytest.MonkeyPatch):
    def post(url: str, *, json: object, timeout: float) -> httpx.Response:
        return httpx.Response(503, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "post", post)

    with pytest.raises(InferenceError, match="HTTP 503") as exc_info:
        OllamaAdapter("http://127.0.0.1:11434", "node-1").generate(_request())

    assert isinstance(exc_info.value.__cause__, httpx.HTTPStatusError)


@pytest.mark.parametrize(
    "body",
    [
        [],
        {"message": []},
        {"message": {"content": 1}},
        {"message": {"content": "ok"}, "eval_count": -1},
        {"message": {"content": "ok"}, "prompt_eval_count": True},
    ],
)
def test_ollama_adapter_rejects_invalid_response(
    monkeypatch: pytest.MonkeyPatch, body: object
):
    def post(url: str, *, json: object, timeout: float) -> httpx.Response:
        return httpx.Response(200, json=body, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "post", post)

    with pytest.raises(InferenceError):
        OllamaAdapter("http://127.0.0.1:11434", "node-1").generate(_request())


def test_ollama_adapter_rejects_non_positive_timeout_without_network():
    with pytest.raises(ValueError, match="timeout_s"):
        OllamaAdapter("http://127.0.0.1:11434", "node-1").generate(
            _request(timeout_s=0)
        )
