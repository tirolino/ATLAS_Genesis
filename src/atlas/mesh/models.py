from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from atlas.guardian.policy import DataClass, TrustTier


class Strategy(str, Enum):
    AUTO = "AUTO"
    SINGLE = "SINGLE"
    DISTRIBUTED = "DISTRIBUTED"
    COLLABORATIVE = "COLLABORATIVE"
    HYBRID = "HYBRID"


@dataclass(frozen=True)
class ModelSpec:
    """Entrada del Model Registry. Solo se enrutan modelos registrados Y aprobados."""

    model_id: str
    family: str
    quantization: str
    weights_bytes: int
    n_layers: int
    n_kv_heads: int
    head_dim: int
    max_context: int
    capabilities: frozenset[str]
    artifact_sha256: str
    approved: bool = False
    # Medido por el Model Evaluator (benchmarks propios), NUNCA autodeclarado por el nodo.
    eval_score: float | None = None
    eval_latency_ms: int | None = None


@dataclass(frozen=True)
class NodeInfo:
    """Estado de un nodo. Las métricas son DECLARACIONES del agente salvo verificación."""

    node_id: str
    trust: TrustTier
    vram_total_bytes: int
    vram_free_bytes: int
    installed_models: frozenset[str]
    healthy: bool = True


@dataclass(frozen=True)
class TaskRequest:
    task_id: str
    task_type: str
    data_class: DataClass
    min_context_tokens: int = 4096
    capabilities: frozenset[str] = frozenset()
    strategy: Strategy = Strategy.AUTO
    concurrency: int = 1
    max_latency_ms: int | None = None


@dataclass(frozen=True)
class Assignment:
    node_id: str
    model_id: str
    estimated_vram_bytes: int
