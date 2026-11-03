# Roadmap revisado

Cambios frente al README original: Guardian y cuarentena de memoria desde la Fase 1; confianza de
nodos antes de cualquier colaboración; benchmarks de continuidad antes de multiplicar modelos.

0. **Diseño**: ADR, definición operativa de identidad y de "continuidad" (ADR-0006), amenazas.
1. **Núcleo determinista + rebanada vertical** (hecho en memoria): audit, guardian, memoria con estados,
   router SINGLE, contrato JSON. Falta: Postgres, Ollama real, API.
2. **Persistence & Recovery**: checkpoints, restauración en entorno limpio, anclaje de la cabeza del log.
3. **Mesh multi-nodo propio (T3)**: agente, heartbeat firmado, registry, DISTRIBUTED por pipeline.
4. **Continuidad y sustitución de modelos**: suite de continuidad como puerta de aprobación.
5. **Confianza de nodos externos**: identidad, T0-T2, benchmarks de reto, revocación.
6. **Colaborativa/Híbrida**: solo si los benchmarks muestran ganancia neta frente a coste.
7. **Learning & Evolution** (solo proponen) con rollback.
8. **Anclaje externo / blockchain y gobernanza**, si hace falta.
9. **Red comunitaria**.
