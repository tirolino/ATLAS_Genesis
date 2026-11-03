"""Model Router del MVP: estrategia SINGLE con filtros duros y heurística de VRAM (ADR-0005).

Orden: (1) filtros obligatorios de seguridad/compatibilidad; (2) ranking por calidad medida,
latencia medida y consumo estimado de VRAM. Las demás estrategias fallan de forma explícita
en lugar de degradarse en silencio.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from atlas.guardian.policy import can_send
from atlas.mesh.models import Assignment, ModelSpec, NodeInfo, Strategy, TaskRequest
from atlas.mesh.resources import estimate_vram_bytes


class NoEligibleCandidate(Exception):
    def __init__(self, reasons: list[str]) -> None:
        super().__init__("; ".join(reasons[:5]) or "sin nodos registrados")
        self.reasons = tuple(reasons)


class UnsupportedStrategy(NotImplementedError):
    pass


_MVP_STRATEGIES = frozenset({Strategy.AUTO, Strategy.SINGLE})


def route(
    task: TaskRequest,
    nodes: Iterable[NodeInfo],
    models: Mapping[str, ModelSpec],
    *,
    safety_margin: float = 0.10,
    supported: frozenset[Strategy] = _MVP_STRATEGIES,
) -> Assignment:
    if task.strategy not in supported:
        raise UnsupportedStrategy(f"estrategia {task.strategy.value} no habilitada todavía")
    if task.max_latency_ms is not None and task.max_latency_ms <= 0:
        raise ValueError("max_latency_ms debe ser mayor que cero")

    reasons: list[str] = []
    candidates: list[tuple[float, float, int, str, str]] = []
    for node in nodes:
        if not node.healthy:
            reasons.append(f"{node.node_id}: no saludable")
            continue
        if not can_send(task.data_class, node.trust):
            reasons.append(
                f"{node.node_id}: {node.trust.name} no autorizado para {task.data_class.name}"
            )
            continue
        budget = node.vram_free_bytes * (1.0 - safety_margin)
        for model_id in sorted(node.installed_models):
            model = models.get(model_id)
            tag = f"{node.node_id}/{model_id}"
            if model is None:
                reasons.append(f"{tag}: modelo no registrado")
            elif not model.approved:
                reasons.append(f"{tag}: modelo no aprobado")
            elif not task.capabilities <= model.capabilities:
                reasons.append(f"{tag}: faltan capacidades")
            elif task.min_context_tokens > model.max_context:
                reasons.append(f"{tag}: contexto insuficiente")
            elif model.eval_latency_ms is not None and model.eval_latency_ms < 0:
                reasons.append(f"{tag}: latencia medida inválida")
            elif task.max_latency_ms is not None and model.eval_latency_ms is None:
                reasons.append(f"{tag}: latencia sin medir")
            elif (
                task.max_latency_ms is not None
                and model.eval_latency_ms is not None
                and model.eval_latency_ms > task.max_latency_ms
            ):
                reasons.append(f"{tag}: latencia superior al límite")
            else:
                est = estimate_vram_bytes(model, task.min_context_tokens, task.concurrency)
                if est > budget:
                    reasons.append(f"{tag}: VRAM insuficiente")
                else:
                    latency = (
                        float(model.eval_latency_ms)
                        if model.eval_latency_ms is not None
                        else float("inf")
                    )
                    candidates.append(
                        (-(model.eval_score or 0.0), latency, est, node.node_id, model_id)
                    )
    if not candidates:
        raise NoEligibleCandidate(reasons)
    _, _, est, node_id, model_id = min(candidates)
    return Assignment(node_id=node_id, model_id=model_id, estimated_vram_bytes=est)
