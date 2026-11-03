import dataclasses
import json
import tempfile
from pathlib import Path

import pytest

from atlas.audit.log import AuditLog, verify_chain
from atlas.shared.crypto import Ed25519Signer


def _log(n=3, path=None):
    signer = Ed25519Signer.generate()
    log = AuditLog(signer, path=path)
    for i in range(n):
        log.append("evt", {"i": i})
    return signer, log


def test_valid_chain_verifies():
    signer, log = _log()
    res = verify_chain(log.entries, {signer.key_id: signer.public_key_raw})
    assert res.ok and res.head_hash == log.head_hash


def test_payload_tampering_detected():
    signer, log = _log()
    entries = list(log.entries)
    entries[1] = dataclasses.replace(entries[1], payload={"i": 999})
    assert not verify_chain(entries, {signer.key_id: signer.public_key_raw}).ok


def test_middle_deletion_detected():
    signer, log = _log(4)
    entries = [e for i, e in enumerate(log.entries) if i != 1]
    assert not verify_chain(entries, {signer.key_id: signer.public_key_raw}).ok


def test_tail_truncation_needs_external_head():
    signer, log = _log(4)
    keys = {signer.key_id: signer.public_key_raw}
    truncated = list(log.entries)[:2]
    assert verify_chain(truncated, keys).ok  # sin ancla externa NO se detecta
    assert not verify_chain(truncated, keys, expected_head=log.head_hash).ok


def test_wrong_key_rejected():
    _, log = _log()
    other = Ed25519Signer.generate()
    assert not verify_chain(log.entries, {other.key_id: other.public_key_raw}).ok


def test_persistence_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "audit.jsonl"
        signer, log = _log(3, path=p)
        reloaded = AuditLog(signer, path=p)
        reloaded.append("evt", {"i": 3})
        assert len(reloaded.entries) == 4
        assert verify_chain(reloaded.entries, {signer.key_id: signer.public_key_raw}).ok
        assert len(p.read_text().splitlines()) == 4
        json.loads(p.read_text().splitlines()[0])


def test_floats_nan_rejected():
    signer = Ed25519Signer.generate()
    with pytest.raises(ValueError):
        AuditLog(signer).append("evt", {"x": float("nan")})
