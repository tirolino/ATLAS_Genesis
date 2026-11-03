---
mode: agent
description: Analiza, planifica, implementa y valida una funcionalidad Python.
---

Implementa la funcionalidad descrita por el usuario siguiendo las instrucciones del repositorio.

1. Inspecciona el código, arquitectura, dependencias y pruebas relacionadas.
2. Resume el comportamiento actual y los cambios necesarios.
3. Para cambios medianos o grandes, escribe un plan en `tasks/todo.md` con archivos afectados, criterios de aceptación, riesgos y pruebas.
4. Implementa el cambio mínimo y mantenible. No refactorices áreas no relacionadas.
5. Añade o actualiza pruebas unitarias, de integración o regresión según corresponda.
6. Ejecuta los controles configurados: Ruff, formato, tipado, pytest y seguridad cuando estén disponibles.
7. Analiza los errores y logs; corrige la causa raíz. Limita la autocorrección a tres iteraciones.
8. Actualiza documentación y marca las tareas completadas.
9. Informa de cambios, validaciones realmente ejecutadas, resultados y pendientes.

No inventes resultados ni elimines pruebas para obtener un resultado satisfactorio. Pide autorización para acciones destructivas o irreversibles.
