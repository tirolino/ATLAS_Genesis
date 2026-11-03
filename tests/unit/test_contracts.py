import json
from pathlib import Path

import pytest

from atlas.cognitive.contracts import DECISION_SCHEMA, ContractViolation, parse_decision

TOOLS = frozenset({"search"})


def test_valid_respond_and_tool():
    assert parse_decision('{"action":"respond","message":"hola"}').message == "hola"
    d = parse_decision('{"action":"call_tool","tool":"search","arguments":{"q":"x"}}', allowed_tools=TOOLS)
    assert d.tool == "search"


@pytest.mark.parametrize("raw", [
    "Claro, aquí tienes: {}",                      # texto libre
    '```json\n{"action":"respond"}\n```',          # fences no se toleran
    "[]",
    '{"action":"hack"}',
    '{"action":"respond","extra":1}',
    '{"action":"call_tool","tool":"rm","arguments":{}}',   # herramienta no permitida
    '{"action":"respond","tool":"search"}',
    '{"action":"respond","message":' + json.dumps("x" * 9000) + "}",
])
def test_fail_closed(raw):
    with pytest.raises(ContractViolation):
        parse_decision(raw, allowed_tools=TOOLS)


def test_exported_schema_in_sync():
    path = Path(__file__).resolve().parents[2] / "contracts" / "schemas" / "decision.schema.json"
    assert json.loads(path.read_text()) == DECISION_SCHEMA
