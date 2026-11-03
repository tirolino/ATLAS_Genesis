---
applyTo: "tests/**/*.py"
---

# Estándares de pruebas

- Usa pytest y nombres `test_<comportamiento>`.
- Prueba resultados y comportamiento observable, no detalles internos.
- Incluye casos normales, límites, entradas inválidas y fallos externos.
- Añade pruebas de regresión para cada bug corregido.
- Aísla red, reloj, filesystem y servicios externos cuando sea apropiado.
- Mantén tests deterministas, independientes y rápidos.
- Usa fixtures pequeñas y explícitas.
- No reduzcas la calidad de las aserciones ni elimines pruebas para hacer pasar la suite.
- No afirmes que una prueba pasa si no se ha ejecutado.
