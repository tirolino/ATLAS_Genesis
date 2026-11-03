"""Detección de GPU vía nvidia-smi. Los valores son DECLARACIONES no verificadas del nodo."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

MIB = 1024**2


@dataclass(frozen=True)
class GpuInfo:
    name: str
    vram_total_bytes: int
    vram_free_bytes: int


def parse_nvidia_smi(output: str) -> list[GpuInfo]:
    gpus: list[GpuInfo] = []
    for line in output.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            continue
        name, total, free = parts
        gpus.append(GpuInfo(name, int(total) * MIB, int(free) * MIB))
    return gpus


def probe_gpus() -> list[GpuInfo]:
    try:
        out = subprocess.run(  # noqa: S603
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free",  # noqa: S607
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return parse_nvidia_smi(out)
