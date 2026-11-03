"""Rebanada vertical en memoria: sin GPU, sin DB, sin red."""

import pytest

from atlas.audit.log import AuditLog, verify_chain
from atlas.cognitive.contracts import ContractViolation
from atlas.cognitive.core import CognitiveCore
from atlas.guardian.policy import DataClass, TrustTier
from atlas.mesh.gateway.fake import FakeInference
from atlas.mesh.gateway.port import InferenceRequest, InferenceResult, InferenceUnavailable
from atlas.mesh.models import ModelSpec, NodeInfo, TaskRequest
from atlas.mesh.resources import GIB
from atlas.mesh.router import NoEligibleCandidate
from atlas.shared.crypto import Ed25519Signer

MODEL = ModelSpec(
    "m", "x", "q4", 2 * GIB, 28, 8, 128, 32768, frozenset(), "sha256:a", approved=True
)


def _core(outputs, trust=TrustTier.T3):
    signer = Ed25519Signer.generate()
    audit = AuditLog(signer)
    node = NodeInfo("n1", trust, 16 * GIB, 14 * GIB, frozenset({"m"}))
    core = CognitiveCore(nodes=lambda: [node], models={"m": MODEL},
                         gateways={"n1": FakeInference("n1", outputs)}, audit=audit)
    return core, audit, {signer.key_id: signer.public_key_raw}


def _task(dc=DataClass.D1):
    return TaskRequest("t1", "chat", dc)


def test_happy_path_is_audited_and_verifiable():
    core, audit, keys = _core(['{"action":"respond","message":"hola"}'])
    assert core.handle(_task(), "saluda").action == "respond"
    assert [e.event_type for e in audit.entries] == [
        "task.received", "inference.completed", "decision.accepted"
    ]
    assert verify_chain(audit.entries, keys).ok
    assert "saluda" not in str([e.payload for e in audit.entries])  # no se loguea el prompt


def test_free_text_is_rejected_and_audited():
    core, audit, _ = _core(["Claro, yo me encargo."])
    with pytest.raises(ContractViolation):
        core.handle(_task(), "haz algo")
    assert audit.entries[-1].event_type == "decision.rejected"


def test_policy_blocks_before_any_inference():
    core, audit, _ = _core([], trust=TrustTier.T1)
    with pytest.raises(NoEligibleCandidate):
        core.handle(_task(DataClass.D3), "secreto")
    assert audit.entries[-1].event_type == "task.unroutable"


def test_inference_unavailability_is_audited_without_prompt_or_response():
    class UnavailableInference:
        def generate(self, request: InferenceRequest) -> InferenceResult:
            raise InferenceUnavailable("motor local no disponible")

    signer = Ed25519Signer.generate()
    audit = AuditLog(signer)
    node = NodeInfo("n1", TrustTier.T3, 16 * GIB, 14 * GIB, frozenset({"m"}))
    core = CognitiveCore(
        nodes=lambda: [node],
        models={"m": MODEL},
        gateways={"n1": UnavailableInference()},
        audit=audit,
    )
    prompt = "contenido sensible"

    with pytest.raises(InferenceUnavailable):
        core.handle(_task(), prompt)

    failure = audit.entries[-1]
    assert failure.event_type == "inference.failed"
    assert failure.payload == {
        "task_id": "t1",
        "node_id": "n1",
        "model_id": "m",
        "error_type": "InferenceUnavailable",
    }
    assert prompt not in str(failure.payload)
