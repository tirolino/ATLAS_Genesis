"""Estimación de VRAM para admisión de tareas (README §9.3).

estimación = pesos + caché KV + sobrecarga del motor
caché KV   = 2 (K y V) * capas * cabezas_kv * dim_cabeza * contexto * bytes_elemento * concurrencia

Es una cota orientativa: la verdad se mide en el nodo (ver Model Evaluator).
"""

from __future__ import annotations

from atlas.mesh.models import ModelSpec

GIB = 1024**3
DEFAULT_ENGINE_OVERHEAD = GIB // 2  # 0,5 GiB


def kv_cache_bytes(
    model: ModelSpec, context_tokens: int, concurrency: int = 1, bytes_per_element: int = 2
) -> int:
    return (
        2 * model.n_layers * model.n_kv_heads * model.head_dim
        * context_tokens * bytes_per_element * concurrency
    )


def estimate_vram_bytes(
    model: ModelSpec,
    context_tokens: int,
    concurrency: int = 1,
    engine_overhead_bytes: int = DEFAULT_ENGINE_OVERHEAD,
) -> int:
    return (
        model.weights_bytes
        + kv_cache_bytes(model, context_tokens, concurrency)
        + engine_overhead_bytes
    )
