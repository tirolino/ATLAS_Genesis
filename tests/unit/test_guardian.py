import pytest

from atlas.guardian.policy import DataClass, PolicyViolation, TrustTier, can_send, require_can_send


def test_matrix():
    assert can_send(DataClass.D0, TrustTier.T0)
    assert not can_send(DataClass.D1, TrustTier.T0)
    assert can_send(DataClass.D2, TrustTier.T2)
    assert not can_send(DataClass.D3, TrustTier.T2)
    assert can_send(DataClass.D3, TrustTier.T3)


def test_require_raises():
    with pytest.raises(PolicyViolation):
        require_can_send(DataClass.D3, TrustTier.T1, node_id="n1")
