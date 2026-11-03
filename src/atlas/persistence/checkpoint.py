"""Manifiesto de checkpoint: raíz de Merkle + firma + enlace al manifiesto anterior.

Merkle con separación de dominio (0x00 hojas / 0x01 nodos internos) y sin duplicar el último
nodo cuando el nivel es impar (evita colisiones por duplicación de hojas).
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from atlas.shared.canonical import canonical_json, hash_object
from atlas.shared.crypto import Signer, verify

GENESIS_MANIFEST = "sha256:" + "0" * 64


def merkle_root(leaves: Sequence[bytes]) -> str:
    if not leaves:
        return "sha256:" + hashlib.sha256(b"").hexdigest()
    level = [hashlib.sha256(b"\x00" + leaf).digest() for leaf in leaves]
    while len(level) > 1:
        nxt: list[bytes] = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                nxt.append(hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest())
            else:
                nxt.append(level[i])
        level = nxt
    return "sha256:" + level[0].hex()


def artifacts_root(artifacts: Mapping[str, str]) -> str:
    """Raíz sobre {nombre: hash}, en orden determinista por nombre."""
    leaves = [f"{name}\x00{h}".encode() for name, h in sorted(artifacts.items())]
    return merkle_root(leaves)


@dataclass(frozen=True)
class Manifest:
    atlas_id: str
    identity_version: int
    memory_version: int
    model_configuration_version: int
    artifacts: dict[str, str]
    merkle_root: str
    previous_manifest: str
    created_at: str
    signer_key_id: str
    signature: str = ""

    def unsigned_body(self) -> dict[str, Any]:
        body = asdict(self)
        del body["signature"]
        return body

    def manifest_hash(self) -> str:
        return hash_object(asdict(self))


def build_manifest(
    *,
    signer: Signer,
    atlas_id: str,
    identity_version: int,
    memory_version: int,
    model_configuration_version: int,
    artifacts: Mapping[str, str],
    previous_manifest: str | None,
    created_at: str,
) -> Manifest:
    unsigned = Manifest(
        atlas_id=atlas_id,
        identity_version=identity_version,
        memory_version=memory_version,
        model_configuration_version=model_configuration_version,
        artifacts=dict(artifacts),
        merkle_root=artifacts_root(artifacts),
        previous_manifest=previous_manifest or GENESIS_MANIFEST,
        created_at=created_at,
        signer_key_id=signer.key_id,
    )
    sig = signer.sign(canonical_json(unsigned.unsigned_body())).hex()
    return Manifest(**{**asdict(unsigned), "signature": sig})


def verify_manifest(
    manifest: Manifest,
    public_keys: Mapping[str, bytes],
    previous: Manifest | None = None,
) -> list[str]:
    errors: list[str] = []
    if artifacts_root(manifest.artifacts) != manifest.merkle_root:
        errors.append("la raíz de Merkle no coincide con los artefactos")
    pub = public_keys.get(manifest.signer_key_id)
    if pub is None:
        errors.append(f"clave desconocida {manifest.signer_key_id}")
    else:
        try:
            sig = bytes.fromhex(manifest.signature)
        except ValueError:
            sig = b""
        if not verify(pub, sig, canonical_json(manifest.unsigned_body())):
            errors.append("firma inválida")
    expected_prev = previous.manifest_hash() if previous else GENESIS_MANIFEST
    if manifest.previous_manifest != expected_prev:
        errors.append("previous_manifest no coincide con el manifiesto anterior")
    return errors
