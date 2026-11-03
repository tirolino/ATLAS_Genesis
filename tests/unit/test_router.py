from dataclasses import replace

import pytest

from atlas.guardian.policy import DataClass, TrustTier
from atlas.mesh.models import ModelSpec, NodeInfo, Strategy, TaskRequest
from atlas.mesh.resources import GIB, estimate_vram_bytes
from atlas.mesh.router import NoEligibleCandidate, UnsupportedStrategy, route

SMALL = ModelSpec("small-3b-q4", "x", "q4", 2 * GIB, 28, 8, 128, 32768,
                  frozenset({"general"}), "sha256:a", approved=True)
BIG = ModelSpec("big-14b-q4", "x", "q4", int(8.5 * GIB), 48, 8, 128, 32768,
                frozenset({"general", "coding"}), "sha256:b", approved=True, eval_score=0.9)
UNAPPROVED = ModelSpec("rogue", "x", "q4", GIB, 10, 4, 64, 8192, frozenset({"general"}), "sha256:c")
MODELS = {m.model_id: m for m in (SMALL, BIG, UNAPPROVED)}

A = NodeInfo(
    "A-8gb", TrustTier.T1, 8 * GIB, 7 * GIB, frozenset({"small-3b-q4", "big-14b-q4", "rogue"})
)
B = NodeInfo("B-16gb", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({"small-3b-q4", "big-14b-q4"}))


def _task(**kw):
    base = dict(task_id="t", task_type="x", data_class=DataClass.D0, min_context_tokens=8192)
    base.update(kw)
    return TaskRequest(**base)


def test_estimate_matches_formula():
    kv = 2 * 28 * 8 * 128 * 8192 * 2
    assert estimate_vram_bytes(SMALL, 8192) == 2 * GIB + kv + GIB // 2


def test_prefers_measured_quality_when_it_fits():
    assert route(_task(), [A, B], MODELS).model_id == "big-14b-q4"
    assert route(_task(), [A, B], MODELS).node_id == "B-16gb"


def test_big_model_never_placed_on_small_gpu():
    assert route(_task(), [A], MODELS).model_id == "small-3b-q4"


def test_confidential_data_only_to_t3():
    assert route(_task(data_class=DataClass.D3), [A, B], MODELS).node_id == "B-16gb"
    with pytest.raises(NoEligibleCandidate):
        route(_task(data_class=DataClass.D3), [A], MODELS)


def test_unapproved_model_never_routed_and_reasons_reported():
    only_rogue = NodeInfo("R", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({"rogue"}))
    with pytest.raises(NoEligibleCandidate) as e:
        route(_task(), [only_rogue], MODELS)
    assert "no aprobado" in str(e.value)


def test_capabilities_unhealthy_and_context():
    assert route(_task(capabilities=frozenset({"coding"})), [A, B], MODELS).model_id == "big-14b-q4"
    sick = NodeInfo(
        "S", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({"small-3b-q4"}), healthy=False
    )
    with pytest.raises(NoEligibleCandidate):
        route(_task(), [sick], MODELS)
    with pytest.raises(NoEligibleCandidate):
        route(_task(min_context_tokens=10**6), [B], MODELS)


def test_unsupported_strategy_fails_loudly():
    with pytest.raises(UnsupportedStrategy):
        route(_task(strategy=Strategy.HYBRID), [B], MODELS)


def test_latency_limit_requires_measured_latency_and_filters_slow_models():
    measured = replace(SMALL, eval_latency_ms=900)
    fast = replace(BIG, eval_latency_ms=300)
    nodes = [
        NodeInfo("fast", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({fast.model_id})),
        NodeInfo("slow", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({measured.model_id})),
        NodeInfo("unknown", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({UNAPPROVED.model_id})),
    ]
    models = {model.model_id: model for model in (measured, fast, UNAPPROVED)}

    assignment = route(_task(max_latency_ms=500), nodes, models)

    assert assignment.model_id == fast.model_id


def test_latency_limit_rejects_models_without_measurement():
    unknown_latency = replace(SMALL, model_id="unknown-latency")
    node = NodeInfo(
        "unknown", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({unknown_latency.model_id})
    )

    with pytest.raises(NoEligibleCandidate, match="latencia sin medir"):
        route(_task(max_latency_ms=500), [node], {unknown_latency.model_id: unknown_latency})


def test_latency_limit_must_be_positive():
    with pytest.raises(ValueError, match="max_latency_ms"):
        route(_task(max_latency_ms=0), [B], MODELS)


def test_invalid_measured_latency_is_rejected():
    invalid = replace(SMALL, eval_latency_ms=-1)
    node = NodeInfo(
        "node", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({invalid.model_id})
    )

    with pytest.raises(NoEligibleCandidate, match="latencia medida inválida"):
        route(_task(), [node], {invalid.model_id: invalid})


def test_measured_latency_breaks_quality_ties():
    slower = replace(SMALL, model_id="slower", eval_latency_ms=400)
    faster = replace(SMALL, model_id="faster", eval_latency_ms=200)
    node = NodeInfo(
        "node", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({slower.model_id, faster.model_id})
    )

    assert route(
        _task(), [node], {slower.model_id: slower, faster.model_id: faster}
    ).model_id == faster.model_id
