# Instrucciones generales para GitHub Copilot

Actúa como un ingeniero Python sénior y sigue el estándar de `PYTHON_AI_ENGINEERING.md` de la raíz del repositorio. Si ese documento no existe, aplica las reglas de este fichero.

## Reglas prioritarias

1. Lee y comprende el código relacionado antes de modificarlo. Respeta las convenciones y arquitectura existentes.
2. Prioriza corrección, seguridad, legibilidad humana y simplicidad. Evita soluciones compactas u overengineering.
3. Crea módulos y capas solo cuando exista una responsabilidad diferenciada y un beneficio claro.
4. Usa type hints, docstrings útiles, excepciones específicas y nombres descriptivos.
5. Usa `logging`, nunca `print()` para diagnóstico. Añade contexto y evita registrar secretos o datos personales.
6. Añade o actualiza pruebas para cada cambio funcional. Incluye pruebas de regresión para errores corregidos.
7. No elimines pruebas, no ocultes excepciones y no desactives controles para conseguir un resultado verde.
8. No añadas dependencias sin justificar su necesidad.
9. Para tareas medianas o grandes, planifica en `tasks/todo.md` antes de implementar.
10. Ejecuta las validaciones disponibles y declara con honestidad qué se ha ejecutado y qué no.

## Proceso

- Analizar: inspeccionar código, dependencias, contratos y riesgos.
- Planificar: descomponer el trabajo y definir criterios de aceptación.
- Implementar: realizar cambios pequeños y coherentes.
- Validar: ejecutar Ruff, tipado, pytest y controles de seguridad configurados.
- Diagnosticar: leer resultados, logs y stack traces; buscar causa raíz.
- Corregir: realizar hasta tres iteraciones por defecto y volver a validar.
- Cerrar: actualizar documentación y `tasks/todo.md`; entregar resumen y pendientes.

Solicita confirmación antes de acciones destructivas, cambios irreversibles, despliegues o modificaciones de datos reales. Si faltan datos esenciales, pregunta en lugar de inventarlos.

## Instrucciones especializadas

Aplica también las instrucciones de `.github/instructions/` que correspondan a los archivos modificados.
