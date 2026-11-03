"""Firma Ed25519. Único módulo que toca claves privadas.

El Cognitive Core NO importa este módulo (contrato en .importlinter): el código que procesa
salidas de un LLM nunca tiene acceso directo a primitivas de firma.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Protocol

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


class Signer(Protocol):
    @property
    def key_id(self) -> str: ...

    def sign(self, data: bytes) -> bytes: ...


def key_id_for(public_key_raw: bytes) -> str:
    return "ed25519:" + hashlib.sha256(public_key_raw).hexdigest()[:16]


class Ed25519Signer:
    def __init__(self, private_key: Ed25519PrivateKey) -> None:
        self._sk = private_key
        self._pub = private_key.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )

    @classmethod
    def generate(cls) -> Ed25519Signer:
        return cls(Ed25519PrivateKey.generate())

    @property
    def public_key_raw(self) -> bytes:
        return self._pub

    @property
    def key_id(self) -> str:
        return key_id_for(self._pub)

    def sign(self, data: bytes) -> bytes:
        return self._sk.sign(data)

    def save_pem(self, path: Path) -> None:
        """Guarda la clave sin cifrar con permisos 0600. SOLO DESARROLLO.

        En producción: KMS/HSM o clave cifrada con passphrase + custodia con quórum.
        """
        pem = self._sk.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as fh:
            fh.write(pem)

    @classmethod
    def load_pem(cls, path: Path) -> Ed25519Signer:
        key = serialization.load_pem_private_key(path.read_bytes(), password=None)
        if not isinstance(key, Ed25519PrivateKey):
            raise ValueError("la clave no es Ed25519")
        return cls(key)


def verify(public_key_raw: bytes, signature: bytes, data: bytes) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(public_key_raw).verify(signature, data)
    except (InvalidSignature, ValueError):
        return False
    return True
