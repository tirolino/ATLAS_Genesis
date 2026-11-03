# Plan de implementación por fases

Este plan convierte el [roadmap](roadmap.md) y los [ADR](adr/) en incrementos pequeños que se
pueden implementar, revisar y verificar antes de avanzar. Está ordenado por dependencias, no por
duración estimada. Una fase se considera terminada solo cuando cumple su criterio de salida; una
función descrita como objetivo no debe darse por implementada hasta que pase esas verificaciones.

## Reglas de ejecución

1. Trabajar en una unidad pequeña por PR: contrato, implementación, pruebas y documentación afectada.
2. No relajar fronteras de módulos ni políticas de seguridad sin revisar o actualizar el ADR pertinente.
3. Mantener el comportamiento seguro por defecto: errores de política, esquema o persistencia no se
   convierten en éxito ni en una degradación silenciosa.
4. Ejecutar las comprobaciones de la fase actual y `make check` antes de integrar, cuando `make` esté
   disponible. El equivalente es Ruff, import-linter, mypy y pytest según `Makefile`.
5. No empezar la fase siguiente hasta cumplir la puerta de salida de la actual. Registrar riesgos,
   límites y resultados medidos en documentación o ADR.

## Fase 0 — Cerrar la línea base de diseño

**Objetivo:** que contratos, alcance y verificaciones estén definidos antes de conectar servicios.

- [ ] Revisar ADR-0001 a ADR-0007 y marcar cuáles están aceptados, reemplazados o aún propuestos.
- [ ] Definir el contrato de configuración local y de despliegue; documentar secretos requeridos sin
  incluir valores reales.
- [ ] Decidir el mecanismo de autenticación de la API y qué datos acepta cada endpoint.
- [ ] Fijar qué eventos pueden entrar en auditoría y confirmar que prompts y respuestas sensibles
  no se registran en claro.
- [ ] Mantener alineados `README.md`, `docs/roadmap.md`, esquemas y este plan.

**Verificación de salida:** las decisiones que bloquean la API o el almacenamiento están escritas
en ADR; una persona nueva puede instalar dependencias y ejecutar las comprobaciones sin necesitar
secretos de producción.

## Fase 1 — Completar el MVP local de extremo a extremo

**Objetivo:** atender una tarea local a través de la API, con política, inferencia y auditoría.

1. [ ] Extraer configuración y composición de dependencias del endpoint; no crear clientes ni claves
   de producción implícitamente al importar la aplicación.
2. [ ] Implementar la autenticación y validación de entrada definidas en la Fase 0. Clasificar la
   tarea antes de seleccionar o invocar un gateway.
3. [ ] Conectar `POST /api/v1/chat` al `CognitiveCore`; responder con errores HTTP explícitos para
   entradas inválidas, política denegada, ausencia de candidatos y fallos del gateway.
4. [ ] Conectar `OllamaAdapter` mediante su puerto, con tiempos límite y salida estructurada. No
   tratar la respuesta del motor como confiable: volver a validar el contrato en el núcleo.
5. [ ] Mantener el gateway falso como camino de prueba rápida; añadir pruebas de API que no
   requieran Ollama y pruebas opcionales de integración con un Ollama real.
6. [ ] Probar respuesta correcta, salida mal formada, herramienta no permitida, nodo no elegible,
   timeout y ausencia del servidor; verificar que cada resultado relevante queda auditado sin
   guardar el prompt ni la respuesta en claro.

**Verificación de salida:** la prueba de integración recorre API → Guardian/Router → gateway falso
→ contrato → auditoría; las pruebas cubren rechazos y fallos, y el endpoint ya no responde 501.
La integración real con Ollama pasa cuando se ejecuta explícitamente con ese servicio disponible.

## Fase 2 — Persistencia PostgreSQL y recuperación

**Objetivo:** hacer durables el estado y la auditoría sin cambiar las reglas deterministas del núcleo.

1. [ ] Definir repositorios tipados para identidad/versiones, memoria/transiciones, auditoría,
   tareas y manifiestos; conservar PostgreSQL como fuente de verdad (ADR-0007).
2. [ ] Aplicar escrituras y cambios de estado en transacciones. Impedir actualizaciones o borrados
   indebidos del log y probar los límites de append-only.
3. [ ] Completar migraciones y validaciones del esquema; probar creación desde una base vacía y
   actualización desde la versión anterior.
4. [ ] Persistir transiciones de memoria con actor, motivo y evidencia. Impedir que el estado guardado
   salte las reglas de cuarentena y aceptación.
5. [ ] Guardar y recuperar manifiestos firmados; validar firma, hashes, encadenamiento y versiones
   antes de restaurar.
6. [ ] Añadir backup y procedimiento de recuperación reproducible, incluyendo referencias a
   artefactos y reconstrucción de índices derivados.

**Verificación de salida:** una prueba de integración con PostgreSQL guarda y lee cada entidad;
una recuperación en una instancia limpia verifica el manifiesto y reconstruye el estado; casos de
corrupción, firma inválida, migración fallida y backup incompleto terminan en error explícito.

## Fase 3 — Mesh propio de un solo nivel de confianza

**Objetivo:** ejecutar tareas `SINGLE` y un pipeline `DISTRIBUTED` solo entre nodos controlados (T3).

1. [ ] Definir identidad de nodo, ciclo de registro/revocación y formato de heartbeat firmado.
2. [ ] Completar el agente de nodo para publicar capacidades y estado; tratar recursos autodeclarados
   como no verificados hasta validarlos.
3. [ ] Añadir registro persistente de nodos, modelos, artefactos (hash y procedencia) y asignaciones.
4. [ ] Conectar las capacidades observadas al router; conservar filtros duros de política,
   aprobación, contexto y VRAM estimada.
5. [ ] Implementar orquestación por pipeline, estados de tarea, idempotencia, timeout y política de
   reintentos. Mantener `COLLABORATIVE` y `HYBRID` deshabilitadas.
6. [ ] Probar dos nodos T3, indisponibilidad durante una tarea, heartbeat obsoleto, revocación,
   recurso insuficiente y resultado no válido.

**Verificación de salida:** el mismo escenario puede ejecutarse contra dos nodos propios; una tarea
no se asigna a un nodo no saludable o revocado, y el reinicio del orquestador no duplica una
asignación ni acepta un resultado sin validar.

## Fase 4 — Continuidad al sustituir modelos

**Objetivo:** convertir el cambio de modelo en una operación evaluada y reversible.

1. [ ] Versionar los casos golden y su procedencia; separar casos `must_pass` de umbrales agregados.
2. [ ] Implementar un runner reproducible que registre modelo, versión, cuantización, configuración
   y resultados sin filtrar datos privados.
3. [ ] Acordar y documentar el umbral mínimo antes de comparar modelos; no cambiarlo para hacer pasar
   una evaluación concreta.
4. [ ] Bloquear la aprobación de un modelo si falla un caso `must_pass` o el umbral acordado.
5. [ ] Probar el cambio a un modelo aprobado y el rollback al anterior sin cambiar identidad,
   constitución ni memoria aceptada.

**Verificación de salida:** la suite puede repetirse con el mismo conjunto versionado; un candidato
que no cumple los umbrales no se puede enrutar como aprobado y cada evaluación deja evidencia
auditable.

## Fase 5 — Confianza de nodos externos

**Objetivo:** ampliar el mesh gradualmente sin tratar la reputación ni las declaraciones del nodo
como prueba de seguridad.

1. [ ] Especificar pruebas de alta y verificación para T0, T1 y T2, identidad criptográfica,
   revocación y caducidad de credenciales.
2. [ ] Aplicar la matriz D0-D3 antes de transmitir contenido y limitar cada clase al nivel autorizado.
3. [ ] Minimizar y redactar datos cuando corresponda; documentar que el nodo receptor ve el prompt
   en claro.
4. [ ] Probar nodos manipulados, claves rotadas o revocadas, mensajes repetidos, métricas falsas y
   cambios de nivel de confianza.
5. [ ] Mantener D2/D3 restringidos a T3 hasta que exista una solución de inferencia confidencial
   probada y revisada.

**Verificación de salida:** pruebas negativas demuestran que los datos restringidos nunca llegan a
nodos no autorizados y que un nodo revocado deja de recibir tareas; la incorporación no concede
acceso por autodeclaración.

## Fase 6 — Colaboración y estrategia híbrida, solo con evidencia

**Objetivo:** habilitar estrategias que usan varios modelos únicamente si mejoran el resultado neto.

1. [ ] Definir benchmarks representativos y una línea base `SINGLE`, incluyendo calidad, latencia,
   coste y fallos correlacionados.
2. [ ] Implementar primero una comparación limitada y acotada; preferir validadores deterministas
   sobre un LLM juez cuando sea viable.
3. [ ] Medir si la mejora compensa coste, latencia y complejidad operativa; fijar criterios antes
   de habilitar tráfico real.
4. [ ] Añadir límites de tareas, presupuesto, tiempo, tamaño de resultados y tratamiento de
   discrepancias.
5. [ ] Mantener explícitamente `UnsupportedStrategy` si no se demuestra una ganancia neta.

**Verificación de salida:** los benchmarks reproducibles muestran una mejora sobre la línea base bajo
los criterios publicados; pruebas de carga y fallos confirman que los límites se respetan. Si no,
las estrategias permanecen deshabilitadas.

## Fase 7 — Learning y Evolution bajo control

**Objetivo:** permitir propuestas de aprendizaje y evolución sin que un modelo modifique por sí
mismo la identidad, las políticas o la memoria aceptada.

1. [ ] Definir propuestas tipadas con autor, fuentes, evidencia, impacto y versión objetivo.
2. [ ] Mantener toda nueva información en cuarentena hasta pasar validaciones y autorizaciones.
3. [ ] Exigir pruebas, aprobación según criticidad y registro de auditoría antes de aplicar cambios.
4. [ ] Implementar rollback probado para cambios de configuración, políticas y memoria.
5. [ ] Verificar que una propuesta rechazada o revertida no cambia el estado activo.

**Verificación de salida:** los flujos de aceptación, rechazo y rollback tienen pruebas; ninguna
salida LLM puede aprobar su propia propuesta ni ejecutar cambios críticos directamente.

## Fase 8 — Anclaje externo, blockchain o gobernanza

**Objetivo:** añadir evidencia externa solo cuando el modelo de amenaza y las necesidades de
gobernanza lo requieran.

1. [ ] Precisar qué riesgo no cubre el log firmado local y quién debe verificar la cabeza publicada.
2. [ ] Probar primero un anclaje externo pequeño (por ejemplo, un testigo independiente o sello de
   tiempo); documentar disponibilidad, rotación y revocación de claves.
3. [ ] Evaluar blockchain y contratos únicamente si se necesita no-equivocación pública o
   gobernanza multiparte que el anclaje existente no resuelve.
4. [ ] Si se aprueba esa necesidad, definir contratos, amenazas, auditoría independiente, despliegue
   de prueba y mecanismo de actualización antes de gestionar fondos o gobernanza real.
5. [ ] No registrar prompts, respuestas privadas, claves ni datos personales en una cadena pública.

**Verificación de salida:** un tercero puede verificar las evidencias publicadas y detectar una
cabeza alterada o truncada; contratos, si existen, pasan pruebas y revisión antes de cualquier
uso con valor real. Si no hay necesidad demostrada, esta fase se cierra sin blockchain.

## Fase 9 — Red comunitaria y operación sostenida

**Objetivo:** abrir participación sin asumir que descentralización garantiza seguridad,
disponibilidad o financiación.

1. [ ] Definir incorporación, permisos, revocación, soporte de incidentes y requisitos de operador.
2. [ ] Medir disponibilidad, recuperación, pérdida de nodos, costes y rendimiento en dominios
   independientes.
3. [ ] Establecer cuotas, presupuestos y transparencia financiera antes de asignar incentivos.
4. [ ] Ejecutar pruebas de caída de proveedor, pérdida de réplica, restauración y respuesta a
   incidentes.
5. [ ] Evaluar distribución de pesos entre GPU solo con un caso de uso, topología y benchmark que
   justifiquen su complejidad; no confundirla con distribución de tareas.

**Verificación de salida:** operadores pueden incorporarse y revocarse de forma reproducible; los
objetivos de disponibilidad, RTO/RPO y redundancia publicados se miden en ejercicios, no se afirman
por diseño. La red no se declara lista para producción hasta cumplir los criterios operativos y de
seguridad correspondientes.

## Relación con el roadmap

Este desglose sigue el orden vigente de `docs/roadmap.md`: núcleo local, persistencia, mesh propio,
continuidad, confianza externa, colaboración condicionada, learning/evolution, anclaje y red
comunitaria. Si cambia ese orden, actualiza ambos documentos y registra el motivo en un ADR cuando
afecte a una decisión arquitectónica.
