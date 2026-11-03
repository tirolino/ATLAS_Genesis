"""Serialización canónica y hashing.

Aproximación a RFC 8785 (JCS): claves ordenadas, sin espacios, UTF-8, sin NaN/Inf.
LIMITACIÓN CONOCIDA: no normaliza floats como exige JCS. Regla del proyecto: los objetos
que se firman/hashean NO contienen floats (usar enteros: milisegundos, bytes, basis points).
Ver ADR-0002.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_object(obj: Any) -> str:
    """Hash con prefijo de algoritmo: ``sha256:<hex>``."""
    return "sha256:" + sha256_hex(canonical_json(obj))
