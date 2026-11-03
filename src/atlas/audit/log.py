"""Log de auditoría encadenado (SHA-256) y firmado (Ed25519).

Qué garantiza: detección de modificación, reordenación o borrado intermedio.
Qué NO garantiza por sí solo: quien posee la clave puede reescribir el log entero, y
un truncado de la cola es indetectable sin una referencia externa. Por eso `verify_chain`
acepta `expected_head`: publica periódicamente la cabeza en un medio que no controles
(repositorio Git firmado, sello RFC 3161, testigo externo, y más adelante una L2).
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from atlas.shared.canonical import hash_object
from atlas.shared.crypto import Signer, verify

GENESIS_HASH = "sha256:" + "0" * 64


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class AuditEntry:
    seq: int
    timestamp: str
    event_type: str
    payload: dict[str, Any]
    prev_hash: str
    signer_key_id: str
    entry_hash: str
    signature: str  # hex

    def body(self) -> dict[str, Any]:
        return {
            "seq": self.seq,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "signer_key_id": self.signer_key_id,
        }


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    errors: tuple[str, ...]
    head_hash: str


class AuditLog:
    def __init__(
        self,
        signer: Signer,
        path: Path | None = None,
        clock: Callable[[], str] = _utc_now,
    ) -> None:
        self._signer = signer
        self._path = path
        self._clock = clock
        self._entries: list[AuditEntry] = []
        if path is not None and path.exists():
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        self._entries.append(AuditEntry(**json.loads(line)))

    @property
    def entries(self) -> tuple[AuditEntry, ...]:
        return tuple(self._entries)

    @property
    def head_hash(self) -> str:
        return self._entries[-1].entry_hash if self._entries else GENESIS_HASH

    def append(self, event_type: str, payload: Mapping[str, Any]) -> AuditEntry:
        # El round-trip JSON garantiza que lo hasheado es exactamente lo persistido.
        clean = json.loads(json.dumps(dict(payload), allow_nan=False))
        body = {
            "seq": len(self._entries),
            "timestamp": self._clock(),
            "event_type": event_type,
            "payload": clean,
            "prev_hash": self.head_hash,
            "signer_key_id": self._signer.key_id,
        }
        entry_hash = hash_object(body)
        entry = AuditEntry(
            **body, entry_hash=entry_hash,
            signature=self._signer.sign(entry_hash.encode("ascii")).hex(),
        )
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(entry), sort_keys=True) + "\n")
                fh.flush()
                os.fsync(fh.fileno())
        self._entries.append(entry)
        return entry


def verify_chain(
    entries: Sequence[AuditEntry],
    public_keys: Mapping[str, bytes],
    expected_head: str | None = None,
) -> VerificationResult:
    """Verifica enlaces, hashes y firmas. `public_keys`: key_id -> clave pública raw."""
    errors: list[str] = []
    prev = GENESIS_HASH
    for i, e in enumerate(entries):
        if e.seq != i:
            errors.append(f"seq {e.seq} en la posición {i}")
        if e.prev_hash != prev:
            errors.append(f"seq {e.seq}: prev_hash no coincide (cadena rota)")
        if hash_object(e.body()) != e.entry_hash:
            errors.append(f"seq {e.seq}: contenido alterado (hash no coincide)")
        pub = public_keys.get(e.signer_key_id)
        if pub is None:
            errors.append(f"seq {e.seq}: clave desconocida {e.signer_key_id}")
        else:
            try:
                sig = bytes.fromhex(e.signature)
            except ValueError:
                sig = b""
            if not verify(pub, sig, e.entry_hash.encode("ascii")):
                errors.append(f"seq {e.seq}: firma inválida")
        prev = e.entry_hash
    if expected_head is not None and expected_head != prev:
        errors.append("la cabeza no coincide con la referencia externa (¿truncado o fork?)")
    return VerificationResult(not errors, tuple(errors), prev)
