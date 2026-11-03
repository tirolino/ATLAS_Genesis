# Issue #5 — Servicio base de Model Mesh y adaptador local

Estado: implementada (Issue abierta con `agent:approved`).

## Alcance aprobado

- Mantener un contrato de inferencia genérico e independiente del proveedor.
- Completar la integración local con Ollama mediante el gateway existente.
- Seleccionar candidatos por los filtros de seguridad/capacidad/contexto/VRAM existentes y
  permitir un límite de latencia opcional basado en métricas medidas.
- Informar explícitamente de timeouts e indisponibilidad del motor; no degradar en silencio.
- Añadir pruebas deterministas del router y del adaptador, y documentar el contrato y el
  enrutamiento.

El MVP usa el adaptador Ollama ya presente. vLLM, reintentos, circuit breakers y estrategias de
enrutamiento distintas de `AUTO`/`SINGLE` quedan fuera de este cambio; ADR-0005 mantiene esas
estrategias deshabilitadas.

## Criterios de aceptación

- [x] El contrato genérico es importable como `InferenceProvider` y no depende de SDKs de motores.
- [x] El adaptador Ollama envía solicitudes locales, respeta timeout/salida estructurada y
  traduce fallos de disponibilidad en un error explícito con causa.
- [x] El router aplica filtros de contexto y latencia solicitada sin alterar el comportamiento
  predeterminado; modelos sin latencia medida no satisfacen un límite explícito.
- [x] Pruebas unitarias cubren rutas exitosas, límites y errores del adaptador y router; se valida
  cobertura superior al 80% cuando la herramienta de cobertura disponible lo permita.
- [x] README documenta el contrato, el comportamiento de enrutamiento y los fallos del gateway.

## Archivos previstos

- `src/atlas/mesh/gateway/port.py`
- `src/atlas/mesh/gateway/ollama.py`
- `src/atlas/mesh/models.py`
- `src/atlas/mesh/router.py`
- `src/atlas/cognitive/core.py` (solo si hace falta conservar evidencia de fallos de inferencia)
- `tests/unit/test_router.py`
- `tests/unit/test_ollama.py`
- `README.md`

## Verificación ejecutada

- `python -m pytest -q` — 54 pruebas pasaron.
- `python -m coverage run --source=atlas.mesh.router,atlas.mesh.gateway.ollama -m pytest -q tests/unit/test_router.py tests/unit/test_ollama.py` y `python -m coverage report --include=src/atlas/mesh/router.py,src/atlas/mesh/gateway/ollama.py` — router 98 %, adaptador Ollama 96 %.
- `python -m ruff check --ignore UP042 src/atlas/mesh src/atlas/cognitive/core.py tests/unit/test_router.py tests/unit/test_ollama.py tests/integration/test_vertical_slice.py` — pasó. Se excluyeron los avisos `UP042` preexistentes sobre enums de cadena.
- `python -m mypy src` — pasó.
- `lint-imports` — pasó; 2 contratos conservados, 0 rotos.
- `make arch typecheck test` — pasó; 54 pruebas.
- `make check` — GNU Make 4.4.1 quedó instalado mediante WinGet y la receta se ejecutó. Falló en `ruff check src tests` por 12 hallazgos preexistentes en `src/atlas/memory/lifecycle.py`, `src/atlas/mesh/models.py`, `src/atlas/mesh/validator.py`, `tests/unit/test_contracts.py` y `tests/unit/test_memory_lifecycle.py`; no se modificaron porque son ajenos al alcance. Los objetivos `arch`, `typecheck` y `test` pasaron de forma independiente.
