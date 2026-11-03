---
agent: agent
description: Revisa código Python en busca de defectos, riesgos y deuda técnica.
---

Realiza una revisión crítica del código indicado.

Prioriza:
- Bugs y errores de lógica.
- Vulnerabilidades y exposición de datos.
- Contratos incorrectos y manejo de excepciones.
- Problemas de concurrencia, recursos y rendimiento demostrables.
- Acoplamiento, dependencias circulares y responsabilidades confusas.
- Falta de pruebas relevantes.
- Legibilidad y documentación de APIs públicas.

Para cada hallazgo indica severidad, archivo/línea, evidencia, impacto y recomendación. Distingue defectos confirmados de riesgos hipotéticos. No hagas cambios automáticamente salvo que el usuario lo solicite. Evita sugerencias puramente estilísticas si Ruff ya las cubre.
