import dataclasses

from atlas.persistence.checkpoint import build_manifest, merkle_root, verify_manifest
from atlas.shared.crypto import Ed25519Signer

ARTS = {"memory.dump": "sha256:aa", "models.lock": "sha256:bb", "policies.json": "sha256:cc"}


def _m(signer, prev=None, arts=ARTS):
    return build_manifest(signer=signer, atlas_id="atlas-001", identity_version=1, memory_version=2,
                          model_configuration_version=3, artifacts=arts, previous_manifest=prev,
                          created_at="2026-11-03T00:00:00Z")


def test_merkle_properties():
    assert merkle_root([b"a", b"b", b"c"]) != merkle_root([b"a", b"b", b"c", b"c"])
    assert merkle_root([b"a", b"b"]) != merkle_root([b"b", b"a"])


def test_valid_chain_of_manifests():
    s = Ed25519Signer.generate()
    keys = {s.key_id: s.public_key_raw}
    m1 = _m(s)
    m2 = _m(s, prev=m1.manifest_hash())
    assert verify_manifest(m1, keys) == []
    assert verify_manifest(m2, keys, previous=m1) == []


def test_tampering_detected():
    s = Ed25519Signer.generate()
    keys = {s.key_id: s.public_key_raw}
    m = _m(s)
    bad_art = dataclasses.replace(m, artifacts={**m.artifacts, "memory.dump": "sha256:ff"})
    assert any("Merkle" in e for e in verify_manifest(bad_art, keys))
    bad_ver = dataclasses.replace(m, memory_version=99)
    assert any("firma" in e for e in verify_manifest(bad_ver, keys))
    m2 = _m(s, prev="sha256:" + "1" * 64)
    assert any("previous" in e for e in verify_manifest(m2, keys, previous=m))
