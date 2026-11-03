"""Niveles de confianza (T0-T3), clasificación de datos (D0-D3) y regla de envío.

IMPORTANTE: los niveles son una política de *control de acceso*, no una garantía criptográfica
de confidencialidad. Un nodo que ejecuta inferencia ve el prompt en claro. Por eso D2/D3 solo
deben salir hacia hardware que controlas (T3) mientras no exista inferencia confidencial real.
"""

from __future__ import annotations

from enum import IntEnum


class TrustTier(IntEnum):
    T0 = 0  # no validado
    T1 = 1  # comunitario
    T2 = 2  # verificado
    T3 = 3  # infraestructura propia / controlada


class DataClass(IntEnum):
    D0 = 0  # público
    D1 = 1  # comunitario / anonimizado
    D2 = 2  # interno
    D3 = 3  # confidencial / crítico


class PolicyViolation(Exception):
    """Operación denegada por política."""


def min_tier_for(data_class: DataClass) -> TrustTier:
    return TrustTier(int(data_class))


def can_send(data_class: DataClass, tier: TrustTier) -> bool:
    return tier >= min_tier_for(data_class)


def require_can_send(data_class: DataClass, tier: TrustTier, *, node_id: str = "?") -> None:
    if not can_send(data_class, tier):
        raise PolicyViolation(
            f"datos {data_class.name} no pueden enviarse al nodo {node_id} ({tier.name})"
        )
