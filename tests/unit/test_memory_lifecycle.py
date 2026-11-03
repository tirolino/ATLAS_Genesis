import pytest

from atlas.guardian.policy import TrustTier
from atlas.memory.lifecycle import (
    ActorKind, InvalidTransition, MemoryCandidate, MemoryKind, MemoryStatus as S, transition,
)


def _cand(trust=TrustTier.T1):
    return MemoryCandidate("m1", "hola", MemoryKind.MODEL_OUTPUT, "node-x", trust)


def _to_validated(c):
    c = transition(c, S.QUARANTINED, actor_kind=ActorKind.COGNITIVE_CORE, actor_id="core", reason="ingesta")
    return transition(c, S.VALIDATED, actor_kind=ActorKind.DETERMINISTIC_VALIDATOR, actor_id="v1", reason="schema ok")


def test_cannot_skip_states():
    with pytest.raises(InvalidTransition):
        transition(_cand(), S.ACCEPTED, actor_kind=ActorKind.HUMAN, actor_id="h", reason="x")


def test_llm_cannot_validate():
    c = transition(_cand(), S.QUARANTINED, actor_kind=ActorKind.COGNITIVE_CORE, actor_id="core", reason="ingesta")
    with pytest.raises(InvalidTransition):
        transition(c, S.VALIDATED, actor_kind=ActorKind.LLM, actor_id="m", reason="parece correcto")


def test_untrusted_source_needs_human_or_evidence():
    c = _to_validated(_cand(TrustTier.T1))
    with pytest.raises(InvalidTransition):
        transition(c, S.ACCEPTED, actor_kind=ActorKind.COGNITIVE_CORE, actor_id="core", reason="ok")
    with pytest.raises(InvalidTransition):
        transition(c, S.ACCEPTED, actor_kind=ActorKind.DETERMINISTIC_VALIDATOR, actor_id="v", reason="ok")
    done = transition(c, S.ACCEPTED, actor_kind=ActorKind.DETERMINISTIC_VALIDATOR, actor_id="v",
                      reason="verificado", evidence_refs=("test:123",))
    assert done.status is S.ACCEPTED and len(done.history) == 3


def test_trusted_source_core_can_accept_and_reason_required():
    c = _to_validated(_cand(TrustTier.T3))
    with pytest.raises(InvalidTransition):
        transition(c, S.ACCEPTED, actor_kind=ActorKind.COGNITIVE_CORE, actor_id="core", reason=" ")
    assert transition(c, S.ACCEPTED, actor_kind=ActorKind.COGNITIVE_CORE, actor_id="core", reason="ok").status is S.ACCEPTED


def test_terminal_states():
    c = transition(_cand(), S.REJECTED, actor_kind=ActorKind.HUMAN, actor_id="h", reason="spam")
    with pytest.raises(InvalidTransition):
        transition(c, S.QUARANTINED, actor_kind=ActorKind.HUMAN, actor_id="h", reason="x")
