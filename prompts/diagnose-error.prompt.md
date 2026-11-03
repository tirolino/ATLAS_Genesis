---
mode: agent
description: Diagnostica un error Python a partir de logs, trazas y código.
---

Investiga el error descrito por el usuario.

1. Reproduce o localiza el fallo si el entorno lo permite.
2. Lee el stack trace completo, logs relacionados y código implicado.
3. Separa hechos observados de hipótesis.
4. Identifica la causa raíz y explica por qué ocurre.
5. Propón la corrección mínima que resuelva la causa, no solo el síntoma.
6. Añade una prueba de regresión que falle antes de la corrección y pase después.
7. Ejecuta pruebas y controles relevantes.
8. Revisa que no se hayan filtrado secretos o datos sensibles en los logs.
9. Informa de evidencias, archivos modificados, comandos ejecutados y limitaciones.

No ocultes excepciones, no cambies tests para evitar el fallo y no afirmes haber reproducido algo que no se haya ejecutado.
