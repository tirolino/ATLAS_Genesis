---
name: python-quality
description: 'Calidad Python de ATLAS Genesis: tipado estricto, Ruff, límites de arquitectura, pytest y validación de cambios. Úsalo al implementar o revisar Python.'
---

# Calidad de Python en ATLAS

- Sigue `requires-python` y la configuración de `pyproject.toml`.
- Mantén interfaces tipadas y funciones claras; evita `Any`, casts innecesarios y abstracciones sin
  necesidad.
- Respeta las fronteras verificadas por import-linter y los puertos/adaptadores existentes.
- Para cambios de lógica, añade pruebas pytest de éxito, límites y errores; usa gateways falsos para
  no requerir Ollama/GPU en unit tests.
- No relajes Guardian, contratos fail-closed, auditoría ni cuarentena de memoria para hacer pasar
  pruebas.
- Ejecuta comprobaciones focalizadas y luego `make check` cuando esté disponible. Informa los
  comandos y resultados reales.
- Consulta [instrucciones Python](../../instructions/python.instructions.md),
  [pruebas](../../instructions/testing.instructions.md) y
  [estándares del proyecto](../../../docs/PYTHON_AI_ENGINEERING.md).
