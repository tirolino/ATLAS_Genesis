# Flujo de trabajo guiado por Issues

El flujo separa análisis, aprobación humana e implementación. Una Issue o un comentario nunca
autoriza por sí solo cambios: la asignación automática solo ocurre tras aplicar la etiqueta
`agent:approved` con permisos suficientes.

## Ciclo

1. Abre una Issue usando una plantilla de error o funcionalidad. No incluyas secretos, claves,
   prompts privados ni datos personales.
2. Usa el prompt [Analizar Issue ATLAS](../.github/prompts/analyze-issue.prompt.md) o el agente
   `issue-analyst`. Debe leer contexto, proponer criterios verificables y registrar un plan en
   `tasks/issue-<numero>.md`, sin modificar producto.
3. Una persona revisa criterios, riesgos y dudas. Resuelve las ambigüedades y aprueba explícitamente
   el alcance antes de continuar.
4. Una persona con permisos `write`, `maintain` o `admin` aplica `agent:approved`. El workflow
   `.github/workflows/issue-agent-coordination.yml` verifica el permiso del actor y asigna Copilot
   coding agent con base `developer`.
5. Copilot trabaja en una rama separada, actualiza el plan, añade pruebas y abre un PR hacia
   `developer` que enlaza la Issue. Los agentes `tester` y `reviewer` pueden realizar comprobaciones
   independientes.
6. El equipo revisa el diff, los checks, los criterios de aceptación y los riesgos. El merge siempre
   es manual; no hay auto-merge.

Al abrir o reabrir una Issue, Actions publica las instrucciones del flujo. La apertura no asigna
Copilot. Si se etiqueta sin permiso suficiente, el workflow no asigna el agente.

## Planes de trabajo

- Issues: `tasks/issue-<numero>.md`, un archivo por Issue para permitir trabajo paralelo.
- Trabajo no asociado a Issue: `tasks/todo.md`.

Los planes no deben copiar secretos ni contenido privado. Actualiza su estado en el PR y conserva
solo decisiones y verificaciones relevantes.

## Configuración requerida en GitHub

1. Issues y GitHub Copilot coding agent deben estar habilitados para el repositorio y la cuenta.
2. Mantener la etiqueta `agent:approved`, color `1D76DB`, descripción «Alcance revisado por una
   persona; autoriza a Copilot a implementar». Ya está creada en este repositorio.
3. Mantener el workflow de coordinación con `administration: read` (para verificar el permiso de
   quien aplica la etiqueta) e `issues: write`; no añadir `contents: write` ni credenciales
   personales.
4. Mantener `developer` como rama de integración y dirigir allí los PR de Issues. Los cambios de
   `developer` a `main` se revisan y fusionan por separado.
5. Si Copilot no está disponible, la asignación falla explícitamente; realiza la implementación de
   forma manual o resuelve la habilitación sin ampliar permisos innecesariamente.

El workflow solo comenta y asigna Issues: no modifica archivos, crea ramas, abre PRs ni integra
cambios. Los textos de Issues son entrada no confiable; Copilot debe respetar las instrucciones del
repositorio.
