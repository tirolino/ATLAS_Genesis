---
applyTo: "**/*.py"
---

# Estándares de código Python

- Sigue PEP 8, PEP 257 y el estilo configurado en `pyproject.toml`.
- Usa nombres descriptivos y type hints en interfaces públicas.
- Escribe funciones pequeñas, cohesivas y fáciles de probar.
- Prefiere claridad a expresiones compactas o trucos del lenguaje.
- Usa `pathlib`, gestores de contexto y APIs estándar seguras.
- Evita argumentos mutables por defecto, estado global mutable y dependencias circulares.
- Captura excepciones específicas; conserva la causa al traducirlas.
- No uses `print()` para logging ni `except Exception` para ocultar errores.
- Documenta contratos, unidades, efectos secundarios y excepciones relevantes.
- Mantén compatibilidad con `requires-python`.
- No añadas abstracciones o clases sin una necesidad demostrable.
