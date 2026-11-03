"""Contrato estricto de las decisiones del LLM (ADR-0003).

El Cognitive Core NO interpreta texto libre para decisiones de control. El LLM debe devolver
JSON conforme a DECISION_SCHEMA; cualquier desviación se rechaza (fail-closed): sin reparar,
sin tolerar bloques markdown, sin claves extra.

Validez de esquema != corrección semántica: sigue haciendo falta validación de contenido.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

ACTIONS = ("respond", "call_tool", "ask_clarification", "refuse")
MAX_MESSAGE_CHARS = 8000

DECISION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["action"],
    "properties": {
        "action": {"type": "string", "enum": list(ACTIONS)},
        "message": {"type": "string", "maxLength": MAX_MESSAGE_CHARS},
        "tool": {"type": "string"},
        "arguments": {"type": "object"},
    },
}


class ContractViolation(ValueError):
    pass


@dataclass(frozen=True)
class Decision:
    action: str
    message: str | None = None
    tool: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)


def parse_decision(raw: str, *, allowed_tools: frozenset[str] = frozenset()) -> Decision:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ContractViolation(f"no es JSON válido: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ContractViolation("la raíz debe ser un objeto")
    extra = set(data) - set(DECISION_SCHEMA["properties"])
    if extra:
        raise ContractViolation(f"claves no permitidas: {sorted(extra)}")
    action = data.get("action")
    if action not in ACTIONS:
        raise ContractViolation("action ausente o fuera de catálogo")
    message = data.get("message")
    if message is not None and (not isinstance(message, str) or len(message) > MAX_MESSAGE_CHARS):
        raise ContractViolation("message inválido")
    tool = data.get("tool")
    arguments = data.get("arguments", {})
    if not isinstance(arguments, dict):
        raise ContractViolation("arguments debe ser un objeto")
    if action == "call_tool":
        if tool not in allowed_tools:
            raise ContractViolation(f"herramienta no permitida: {tool!r}")
    elif tool is not None or arguments:
        raise ContractViolation("tool/arguments solo se admiten con call_tool")
    return Decision(action=action, message=message, tool=tool, arguments=arguments)
