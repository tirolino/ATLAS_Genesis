# Contribuir

Cambios pequeños, con tests y documentación. Flujo: Issue → análisis y criterios de aceptación →
aprobación humana → rama de trabajo y PR hacia `developer` → revisión → integración manual.
Consulta [el flujo de trabajo de Issues y Copilot](docs/ISSUE_WORKFLOW.md).

Usa `make check` antes de abrir un PR. Las decisiones de arquitectura se registran como ADR en
`docs/adr/`. Nunca incluyas secretos, claves, datos personales ni artefactos de modelos sin
licencia/procedencia verificadas. Las fronteras de `.importlinter` no se relajan sin un ADR.
