# ATLAS Genesis

> **Una inteligencia artificial persistente, evolutiva y distribuida,
> diseñada para conservar su identidad y memoria mientras sustituye,
> incorpora y coordina diferentes modelos de IA.**

**Estado:** diseño y especificación inicial\
**Versión de documentación:** 1.0\
**Fecha:** 2 de noviembre de 2026\
**Licencia:** por decidir

------------------------------------------------------------------------

## Índice

-   [1. Visión del proyecto](#1-visión-del-proyecto)
-   [2. Objetivos y principios](#2-objetivos-y-principios)
-   [3. Qué significa persistencia](#3-qué-significa-persistencia)
-   [4. Arquitectura general](#4-arquitectura-general)
-   [5. ATLAS Model Mesh](#5-atlas-model-mesh)
-   [6. Estrategias de inferencia](#6-estrategias-de-inferencia)
-   [7. Red de nodos y niveles de
    confianza](#7-red-de-nodos-y-niveles-de-confianza)
-   [8. Clasificación y protección de
    datos](#8-clasificación-y-protección-de-datos)
-   [9. Gestión de modelos y hardware](#9-gestión-de-modelos-y-hardware)
-   [10. Componentes y
    responsabilidades](#10-componentes-y-responsabilidades)
-   [11. Tecnologías propuestas](#11-tecnologías-propuestas)
-   [12. Modelo de datos](#12-modelo-de-datos)
-   [13. API](#13-api)
-   [14. Blockchain y economía
    comunitaria](#14-blockchain-y-economía-comunitaria)
-   [15. Seguridad](#15-seguridad)
-   [16. Persistencia, recuperación y
    continuidad](#16-persistencia-recuperación-y-continuidad)
-   [17. Requisitos no funcionales](#17-requisitos-no-funcionales)
-   [18. Roadmap](#18-roadmap)
-   [19. Criterios de aceptación](#19-criterios-de-aceptación)
-   [20. Riesgos y limitaciones](#20-riesgos-y-limitaciones)
-   [21. Estructura prevista del
    repositorio](#21-estructura-prevista-del-repositorio)
-   [22. Cómo contribuir](#22-cómo-contribuir)
-   [23. Glosario](#23-glosario)
-   [24. Referencias técnicas](#24-referencias-técnicas)

------------------------------------------------------------------------

## 1. Visión del proyecto

**ATLAS Genesis** es una propuesta de arquitectura para construir una
inteligencia artificial persistente, evolutiva y distribuida.

Su característica principal es que la identidad, la memoria, el
historial y las reglas de continuidad de ATLAS no dependen de un único
modelo de lenguaje (LLM), proveedor, servidor o nodo.

ATLAS podrá incorporar diferentes modelos de código abierto, ejecutarlos
en hardware heterogéneo y seleccionar dinámicamente qué modelo o
conjunto de modelos utilizar para cada tarea.

La arquitectura contempla:

-   Una identidad nuclear estable y una identidad evolutiva versionada.
-   Memoria persistente, estructurada y semántica.
-   Aprendizaje y evolución sometidos a evaluación y controles.
-   Un conjunto distribuido de nodos con diferentes capacidades.
-   Coordinación de múltiples LLM mediante **ATLAS Model Mesh**.
-   Persistencia redundante y procedimientos de recuperación.
-   Blockchain para registrar evidencias, identidad, gobernanza y
    eventos relevantes.
-   Financiación y participación comunitarias, sujetas a reglas
    transparentes.

### 1.1. Qué no pretende ser

ATLAS no presupone que almacenar datos en una blockchain genere
conciencia, inteligencia o inmortalidad. Tampoco presupone que una
colección de LLM coordinados constituya automáticamente una inteligencia
superior.

El proyecto busca continuidad operativa y cognitiva verificable, no
demostrar conciencia artificial.

------------------------------------------------------------------------

## 2. Objetivos y principios

### 2.1. Objetivos

1.  Mantener una identidad verificable independiente de los LLM
    utilizados.
2.  Conservar memoria e historial de forma persistente y recuperable.
3.  Incorporar y sustituir modelos sin perder continuidad.
4.  Distribuir tareas entre nodos con distintas GPU, CPU y memoria.
5.  Utilizar varios modelos para colaborar y contrastar resultados.
6.  Permitir la participación comunitaria con permisos diferenciados.
7.  Proteger la información privada y las operaciones críticas.
8.  Evitar dependencias absolutas de un proveedor o infraestructura.
9.  Hacer auditables las modificaciones de identidad, modelos y
    políticas.
10. Evolucionar mediante cambios versionados, evaluados y reversibles.

### 2.2. Principios arquitectónicos

  -----------------------------------------------------------------------
  Principio                           Aplicación
  ----------------------------------- -----------------------------------
  Independencia del modelo            La identidad no depende de un LLM
                                      concreto.

  Modularidad                         Cada motor puede sustituirse
                                      mediante interfaces estables.

  Portabilidad                        Los datos y artefactos deben poder
                                      exportarse y recuperarse.

  Seguridad por diseño                Los permisos se aplican antes de
                                      ejecutar tareas.

  Confianza graduada                  Los nodos reciben acceso según su
                                      nivel de verificación.

  Trazabilidad                        Las ejecuciones identifican modelo,
                                      versión, nodo y configuración.

  Tolerancia a fallos                 La caída de un nodo no debe detener
                                      toda la red.

  Evolución controlada                Los cambios se evalúan, versionan y
                                      pueden revertirse.

  Transparencia                       Las decisiones relevantes dejan
                                      evidencia auditable.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Qué significa persistencia

En ATLAS, la persistencia se define como la capacidad de reconstruir una
instancia funcional a partir de información, artefactos y reglas de
continuidad verificables.

Se distinguen cuatro dimensiones:

1.  **Persistencia de identidad:** identificador, claves, genealogía,
    reglas nucleares y versiones.
2.  **Persistencia de memoria:** hechos, experiencias, conocimientos,
    procedencia y relaciones.
3.  **Persistencia de capacidades:** modelos, herramientas,
    configuraciones y evaluaciones.
4.  **Persistencia operativa:** posibilidad de desplegar y recuperar
    ATLAS en otros nodos.

La continuidad no está garantizada por una blockchain o por IPFS por sí
solos. Requiere réplicas, operadores, financiación, copias verificadas,
claves recuperables y procedimientos probados.

------------------------------------------------------------------------

## 4. Arquitectura general

La arquitectura se divide en módulos independientes coordinados por un
núcleo central lógico.

``` mermaid
flowchart TB
    CC["Cognitive Core"]
    ID["Identity Engine"]
    MEM["Memory Engine"]
    LE["Learning Engine"]
    EV["Evolution Engine"]
    PM["Persistence & Recovery"]
    BM["Blockchain Engine"]
    ECO["Economy Engine"]
    GUARD["Guardian"]
    MESH["ATLAS Model Mesh"]

    CC <--> MESH
    CC <--> MEM
    CC <--> LE
    LE <--> EV
    EV <--> ID
    MEM <--> PM
    ID <--> BM
    ECO <--> BM
    GUARD -. políticas y permisos .-> CC
    GUARD -. políticas y permisos .-> MESH
    GUARD -. políticas y permisos .-> EV
```

### 4.1. Módulos principales

  -----------------------------------------------------------------------
  Módulo                              Responsabilidad
  ----------------------------------- -----------------------------------
  Cognitive Core                      Coordina razonamiento, objetivos y
                                      ejecución de tareas.

  Identity Engine                     Gestiona identidad, claves,
                                      genealogía y versiones.

  Memory Engine                       Gestiona memoria estructurada y
                                      semántica.

  Learning Engine                     Evalúa y procesa nuevas
                                      experiencias y conocimientos.

  Evolution Engine                    Propone y controla cambios
                                      evolutivos.

  Persistence & Recovery              Crea checkpoints y reconstruye
                                      instancias.

  Blockchain Engine                   Registra evidencias y eventos
                                      verificables.

  Economy Engine                      Gestiona financiación y recursos
                                      comunitarios.

  Guardian                            Aplica políticas de seguridad y
                                      autorización.

  Model Mesh                          Descubre, evalúa y coordina modelos
                                      y nodos.
  -----------------------------------------------------------------------

### 4.2. Separación de responsabilidades

El LLM no será la autoridad sobre la identidad, las claves, los permisos
o la memoria persistente. Los modelos producen resultados; los servicios
deterministas aplican políticas, verifican operaciones y controlan qué
información se conserva.

------------------------------------------------------------------------

## 5. ATLAS Model Mesh

**ATLAS Model Mesh** es la infraestructura de inferencia heterogénea y
distribuida de ATLAS.

Su finalidad es permitir que diferentes modelos, versiones,
cuantizaciones y motores de inferencia colaboren sin que ATLAS dependa
de un único modelo.

### 5.1. Decisiones adoptadas

  Decisión                          Selección
  --------------------------------- ------------------------------
  Estrategia de inferencia          `BOTH`
  Participación de nodos            `TIERED TRUST`
  Arquitectura                      Heterogénea y distribuida
  Selección                         Dinámica según tarea
  Distribución de pesos entre GPU   Fase posterior
  Identidad de ATLAS                Independiente de los modelos

### 5.2. Componentes

**Model Registry**

Catálogo de modelos y artefactos:

-   Familia, nombre, versión y arquitectura.
-   Número de parámetros.
-   Cuantización y formato de pesos.
-   Capacidades declaradas y evaluadas.
-   Licencia y procedencia.
-   Hash de artefactos.
-   Estado de aprobación o revocación.
-   Compatibilidad con motores y hardware.

**Node Capability Manager**

Inventario y monitorización de nodos:

-   Identidad criptográfica.
-   GPU, VRAM total y disponible.
-   CPU y RAM.
-   Motores instalados.
-   Modelos disponibles y cargados.
-   Carga, temperatura y disponibilidad.
-   Métricas observadas de inferencia.
-   Heartbeat y estado de conexión.

**Model Router**

Selecciona el modelo y el nodo adecuados. Primero aplica filtros
obligatorios de seguridad, privacidad y compatibilidad; después compara
calidad, latencia, coste y especialización.

**Task Orchestrator**

Descompone tareas, establece dependencias, ejecuta subtareas en
paralelo, gestiona reintentos y reúne resultados.

**Inference Gateway**

Unifica la comunicación con motores de inferencia mediante adaptadores.
Los primeros candidatos son Ollama, llama.cpp y vLLM.

**Model Evaluator**

Ejecuta benchmarks y registra calidad, latencia, tokens por segundo,
consumo de memoria y rendimiento por categoría.

**Trust & Policy Engine**

Controla niveles de confianza, autorización, clasificación de datos y
revocación.

**Model Result Validator**

Distingue entre resultado recibido, resultado validado y resultado
aceptado por Cognitive Core.

**Mesh Observability**

Proporciona métricas, trazas, logs y correlación de ejecuciones.

### 5.3. Arquitectura del Model Mesh

``` mermaid
flowchart TB
    CORE["ATLAS Cognitive Core"]
    ROUTER["Model Router"]
    ORCH["Task Orchestrator"]
    REG["Model Registry"]
    NODE["Node Capability Manager"]
    TRUST["Trust & Policy Engine"]
    VALID["Model Result Validator"]
    GW["Inference Gateway"]

    CORE --> ROUTER
    ROUTER <--> REG
    ROUTER <--> NODE
    ROUTER <--> TRUST
    ROUTER --> ORCH
    ORCH --> GW
    GW --> N1["Node A · GPU 8 GB"]
    GW --> N2["Node B · GPU 12–16 GB"]
    GW --> N3["Node C · GPU 24 GB+"]
    N1 --> VALID
    N2 --> VALID
    N3 --> VALID
    VALID --> CORE
```

### 5.4. Estrategias de inferencia

#### SINGLE

Una tarea se ejecuta en un único modelo. Adecuada para operaciones
sencillas o cuando distribuir no aporta valor.

#### DISTRIBUTED --- Task Distribution

Una tarea se divide en subtareas que se asignan a modelos diferentes.

Ejemplo: análisis de un repositorio mediante tareas separadas de
inventario, análisis de código, revisión de arquitectura y pruebas.

#### COLLABORATIVE --- Collaborative Inference

Varios modelos reciben la misma tarea o variantes controladas y producen
respuestas independientes. Un evaluador compara resultados y
discrepancias.

La coincidencia entre modelos no se considera prueba suficiente de
veracidad.

#### HYBRID

Combina distribución y colaboración. Una tarea se descompone y las
subtareas críticas pueden recibir varias evaluaciones independientes.

El router puede seleccionar automáticamente `SINGLE`, `DISTRIBUTED`,
`COLLABORATIVE` o `HYBRID`.

### 5.5. Ejemplo de distribución por hardware

Los perfiles siguientes son orientativos, no límites garantizados:

  -----------------------------------------------------------------------
  Recursos GPU            Perfil de modelos a     Tareas posibles
                          explorar                
  ----------------------- ----------------------- -----------------------
  8 GB VRAM               1B--3B cuantizados      Clasificación,
                                                  extracción, resúmenes

  12 GB VRAM              7B--8B cuantizados      Asistencia general y
                                                  código sencillo

  16 GB VRAM              7B--14B, según          Análisis y programación
                          cuantización            

  24 GB VRAM              14B o modelos mayores   Análisis exigente y
                          muy cuantizados         evaluación

  48 GB o más             Modelos mayores, según  Inferencia de mayor
                          arquitectura            capacidad
  -----------------------------------------------------------------------

La compatibilidad debe estimarse considerando pesos, cuantización, caché
KV, longitud de contexto, concurrencia y memoria adicional del motor. No
se debe seleccionar un modelo únicamente por su número de parámetros.

### 5.6. Distribución de tareas frente a distribución de pesos

Son capacidades distintas:

-   **Distribución de tareas:** cada nodo ejecuta su propio modelo y
    recibe trabajos independientes. Es la estrategia inicial
    recomendada.
-   **Distribución de un modelo:** los pesos de un único modelo se
    reparten entre varias GPU mediante técnicas como tensor parallelism
    o pipeline parallelism. Se pospone hasta disponer de una red y
    hardware adecuados.

------------------------------------------------------------------------

## 6. Estrategias de ejecución: ejemplo

Solicitud: «Analiza este repositorio, identifica problemas y propón una
solución».

``` mermaid
flowchart TD
    A["Solicitud del usuario"] --> B["Cognitive Core"]
    B --> C["Clasificar tarea y datos"]
    C --> D["Model Router"]
    D --> E["Descomponer tarea"]
    E --> F["Nodo pequeño: inventario"]
    E --> G["Nodo intermedio: análisis de código"]
    E --> H["Nodo potente: arquitectura"]
    F --> I["Integrar resultados"]
    G --> I
    H --> I
    I --> J["Colaboración adicional si es necesaria"]
    J --> K["Validación"]
    K --> L["Cognitive Core"]
    L --> M["Decisión y memoria"]
```

El sistema debe evitar ejecutar modelos adicionales cuando el coste de
coordinación supere el beneficio esperado.

------------------------------------------------------------------------

## 7. Red de nodos y niveles de confianza

La red utiliza cuatro niveles de confianza.

  --------------------------------------------------------------------------
  Nivel                   Descripción             Uso permitido
  ----------------------- ----------------------- --------------------------
  T0 --- Untrusted        Nodo externo no         Datos públicos o
                          validado                sintéticos

  T1 --- Community        Nodo registrado por la  Datos públicos y
                          comunidad               autorizados/anonimizados

  T2 --- Verified         Nodo que ha superado    Datos internos autorizados
                          verificaciones          según política

  T3 --- Core Trusted     Infraestructura         Operaciones y datos
                          controlada y autorizada confidenciales autorizados
  --------------------------------------------------------------------------

El nivel de confianza no se concede por autodeclaración. La reputación
es una señal complementaria y no sustituye la verificación.

### 7.1. Registro y verificación

Cada nodo tendrá:

-   Identificador único.
-   Clave pública.
-   Información de hardware y software.
-   Agente de nodo.
-   Heartbeat.
-   Modelos instalados.
-   Historial de evaluaciones.
-   Nivel de confianza.
-   Estado de autorización y revocación.

Las métricas comunicadas por un nodo pueden ser manipuladas. Deben
considerarse declaraciones del agente salvo que exista un mecanismo
independiente de comprobación.

------------------------------------------------------------------------

## 8. Clasificación y protección de datos

La clasificación se aplica antes de enviar una tarea a un nodo.

  Clasificación   Descripción                 Niveles autorizables
  --------------- --------------------------- ----------------------
  D0              Público                     T0--T3
  D1              Comunitario o anonimizado   T1--T3
  D2              Interno                     T2--T3
  D3              Confidencial o crítico      T3

La política concreta debe determinar qué datos pueden salir de cada
entorno. La clasificación no sustituye el análisis legal, contractual o
de privacidad que corresponda.

Reglas:

-   No enviar secretos, credenciales o claves privadas a los LLM.
-   Minimizar el contexto enviado.
-   Aplicar redacción de información sensible.
-   Cifrar comunicaciones y almacenamiento.
-   Restringir acceso y retención.
-   No incorporar automáticamente resultados comunitarios a la memoria
    permanente.
-   Mantener separación entre contenido recibido y políticas de
    ejecución.

------------------------------------------------------------------------

## 9. Gestión de modelos y hardware

### 9.1. Metadatos de modelos

Cada modelo debe registrar:

-   Identificador y nombre.
-   Familia y proveedor.
-   Versión exacta.
-   Arquitectura.
-   Parámetros.
-   Cuantización.
-   Formato y hash de pesos.
-   Licencia.
-   Procedencia.
-   Capacidades.
-   Contexto máximo probado.
-   Motores compatibles.
-   Resultados de benchmarks.

### 9.2. Metadatos de nodos

Cada nodo debe registrar:

-   GPU y fabricante.
-   VRAM total y disponible.
-   CPU y RAM.
-   Sistema operativo.
-   Motores de inferencia y versiones.
-   Modelos instalados.
-   Modelos cargados.
-   Carga y temperatura.
-   Rendimiento observado.
-   Nivel de confianza.
-   Restricciones de ejecución.

### 9.3. Admisión de una tarea

Antes de asignar una inferencia, el router debe estimar:

1.  Memoria de pesos.
2.  Memoria de caché KV.
3.  Contexto solicitado.
4.  Concurrencia prevista.
5.  Memoria adicional del motor.
6.  Recursos reservados para otras tareas.

Debe existir margen de seguridad configurable. La disponibilidad de VRAM
cambia dinámicamente.

------------------------------------------------------------------------

## 10. Componentes y responsabilidades

### 10.1. Cognitive Core

Interpreta solicitudes, establece objetivos y decide qué capacidades
necesita. No debe gestionar directamente las claves ni saltarse las
políticas del Guardian.

### 10.2. Identity Engine

Gestiona DID, claves, versiones, genealogía y reglas de continuidad. La
identidad nuclear debe estar protegida frente a modificaciones
unilaterales del LLM.

### 10.3. Memory Engine

Gestiona memoria estructurada, memoria semántica, procedencia, versiones
y retención.

### 10.4. Learning Engine

Evalúa información y experiencias nuevas. Distingue hechos, hipótesis,
resultados de modelos y conocimientos validados.

### 10.5. Evolution Engine

Propone cambios en objetivos, estrategias, capacidades y configuración.
Los cambios pasan por evaluación, pruebas, autorización según criticidad
y posibilidad de rollback.

### 10.6. Persistence & Recovery Engine

Crea checkpoints, verifica manifiestos, gestiona réplicas y permite
reconstruir una instancia.

### 10.7. Blockchain Engine

Registra evidencias, hashes, eventos de identidad y gobernanza. No aloja
el cerebro ni el contenido privado de las inferencias.

### 10.8. Economy Engine

Gestiona financiación comunitaria, tesorería, asignación de recursos y
rendición de cuentas. La primera versión no requiere un token
especulativo.

### 10.9. Guardian

Aplica permisos, límites de gasto, políticas de datos, autorización de
herramientas y controles de operaciones críticas.

------------------------------------------------------------------------

## 11. Tecnologías propuestas

La selección es una propuesta inicial y debe validarse mediante
prototipos y ADR.

  -----------------------------------------------------------------------
  Área                    Tecnología candidata    Uso
  ----------------------- ----------------------- -----------------------
  Backend                 Python 3.12+            Servicios y
                                                  orquestación

  API                     FastAPI                 Interfaces REST

  Inferencia local        Ollama                  Prototipos y
                                                  despliegues sencillos

  Inferencia optimizada   llama.cpp               Modelos cuantizados y
                                                  GGUF

  Inferencia GPU          vLLM                    Servidores de
                                                  inferencia de alto
                                                  rendimiento

  Datos relacionales      PostgreSQL              Estado y metadatos

  Vector database         Qdrant                  Recuperación semántica

  Mensajería              NATS o Redis Streams    Colas y eventos

  Almacenamiento          IPFS/Kubo               Distribución
                                                  direccionada por
                                                  contenido

  Archivo                 Filecoin u otro         Persistencia de
                          almacenamiento          artefactos
                          redundante              

  Identidad               DID y Ed25519           Identidad y firmas

  Integridad              SHA-256 y Merkle trees  Verificación

  Smart contracts         Solidity / EVM L2       Registro y gobernanza

  Contratos de desarrollo Foundry                 Pruebas y despliegue

  Contenedores            Docker / Compose        Entornos reproducibles

  Observabilidad          Prometheus / Grafana /  Métricas y trazas
                          OpenTelemetry           

  Workflows durables      Temporal                Procesos recuperables
  -----------------------------------------------------------------------

### 11.1. Abstracción de inferencia

El Cognitive Core debe comunicarse con un contrato común. Los
adaptadores traducen ese contrato a la API de cada motor.

Esto permite sustituir Ollama por llama.cpp o vLLM sin cambiar la lógica
de negocio.

------------------------------------------------------------------------

## 12. Modelo de datos

PostgreSQL será la fuente de verdad para identidad, catálogo, tareas,
asignaciones, políticas y auditoría.

Qdrant almacenará embeddings y datos de recuperación semántica, pero no
será la fuente de verdad.

### 12.1. Entidades de identidad y memoria

-   `atlas_identity`
-   `identity_versions`
-   `memories`
-   `memory_versions`
-   `learning_tasks`
-   `evolution_proposals`
-   `checkpoints`
-   `storage_replicas`

### 12.2. Entidades del Model Mesh

  Tabla                     Responsabilidad
  ------------------------- ---------------------------------------
  `mesh_nodes`              Identidad, estado y hardware de nodos
  `mesh_models`             Catálogo de modelos y versiones
  `mesh_node_models`        Modelos instalados en cada nodo
  `mesh_tasks`              Tareas y estrategia
  `mesh_task_assignments`   Ejecuciones asignadas
  `mesh_results`            Resultados y validaciones
  `mesh_evaluations`        Benchmarks y métricas
  `mesh_trust_events`       Historial de confianza
  `mesh_policies`           Políticas de ejecución

### 12.3. Reglas de persistencia

-   Los registros críticos tendrán identificadores estables.
-   Los cambios relevantes se versionarán.
-   Los resultados conservarán procedencia.
-   Las políticas y niveles de confianza tendrán historial.
-   Se evitará guardar indiscriminadamente prompts y respuestas
    sensibles.
-   Las operaciones de escritura deberán ser idempotentes cuando
    corresponda.

------------------------------------------------------------------------

## 13. API

Todas las APIs estarán versionadas y protegidas.

### 13.1. API general

Prefijo: `/api/v1`

  Endpoint                 Método   Función
  ------------------------ -------- -----------------------------
  `/identity`              GET      Consultar identidad
  `/identity/history`      GET      Historial de identidad
  `/chat`                  POST     Interacción
  `/memory`                POST     Incorporar memoria
  `/memory/search`         POST     Buscar memoria
  `/learning/tasks`        POST     Crear tarea de aprendizaje
  `/evolution/proposals`   POST     Proponer evolución
  `/checkpoints`           POST     Crear checkpoint
  `/checkpoints/latest`    GET      Consultar último checkpoint
  `/recovery/verify`       POST     Verificar recuperación
  `/recovery/restore`      POST     Restaurar instancia

### 13.2. API Model Mesh

Prefijo: `/api/v1/mesh`

  Endpoint                     Método     Función
  ---------------------------- ---------- -----------------------------
  `/nodes/register`            POST       Registrar nodo
  `/nodes/{id}/heartbeat`      POST       Actualizar estado
  `/nodes/{id}/trust`          GET        Consultar confianza
  `/nodes/{id}/trust/review`   POST       Solicitar revisión
  `/nodes/{id}/trust/revoke`   POST       Revocar nodo
  `/models/register`           POST       Registrar modelo
  `/models`                    GET        Buscar modelos
  `/tasks`                     POST       Crear tarea de inferencia
  `/tasks/{id}`                GET        Consultar tarea
  `/tasks/{id}/results`        GET        Consultar resultados
  `/evaluations/run`           POST       Ejecutar benchmark
  `/policies`                  GET/POST   Consultar o crear políticas
  `/policies/{id}`             PUT        Actualizar política

### 13.3. Ejemplo de solicitud de inferencia

``` json
{
  "task_type": "code_analysis",
  "strategy": "AUTO",
  "requirements": {
    "reasoning_level": "HIGH",
    "min_context_tokens": 16000,
    "capabilities": ["coding", "reasoning"]
  },
  "data_classification": "D1",
  "constraints": {
    "max_latency_seconds": 120,
    "max_cost": 0.10,
    "min_trust_level": "T1"
  },
  "payload": {
    "repository_context": "..."
  }
}
```

Respuesta orientativa:

``` json
{
  "task_id": "uuid",
  "strategy_selected": "HYBRID",
  "status": "QUEUED",
  "estimated_assignments": 3
}
```

Las estimaciones no son garantías. Los contratos definitivos deberán
publicarse mediante OpenAPI y validarse con pruebas de contrato.

------------------------------------------------------------------------

## 14. Blockchain y economía comunitaria

### 14.1. Uso de blockchain

Blockchain se utilizará como capa de verificación y coordinación, no
como almacenamiento del modelo o de la memoria completa.

Posibles contratos:

-   `AtlasRegistry`: identidad y registro de instancias.
-   `AtlasTreasury`: tesorería comunitaria.
-   `AtlasGovernance`: propuestas y votaciones.
-   `AtlasServiceRegistry`: registro de servicios y operadores.

Eventos que podrían registrarse:

-   Altas y revocaciones relevantes.
-   Hashes de manifiestos.
-   Versiones de políticas.
-   Decisiones de gobernanza.
-   Evidencias de checkpoints.

No se publicarán prompts, respuestas privadas, credenciales ni
información personal en una blockchain pública.

### 14.2. Economía comunitaria

La financiación debe priorizar transparencia y sostenibilidad.

Posibles mecanismos:

-   Donaciones.
-   Subvenciones.
-   Patrocinios.
-   Aportaciones de operadores.
-   Recompensas por servicios medidos.
-   Tesorería con límites y autorizaciones.

No se considera necesario emitir un token especulativo en la primera
versión.

------------------------------------------------------------------------

## 15. Seguridad

### 15.1. Principios

-   Mínimo privilegio.
-   Separación de claves.
-   Autorización explícita.
-   Cifrado en tránsito y almacenamiento.
-   Auditoría.
-   Revocación.
-   Aislamiento de ejecución.
-   Validación de entradas y salidas.
-   Protección frente a prompt injection.
-   Control de herramientas y efectos externos.

### 15.2. Claves

Las claves raíz no estarán disponibles para los LLM.

Se separarán:

-   Claves de identidad.
-   Claves operativas.
-   Claves de recuperación.
-   Claves de firma de artefactos.

La recuperación deberá contemplar rotación, revocación, custodia y
procedimientos de quórum.

### 15.3. Riesgos específicos del Model Mesh

  -----------------------------------------------------------------------
  Riesgo                              Control
  ----------------------------------- -----------------------------------
  Nodo malicioso                      Niveles de confianza, aislamiento y
                                      auditoría

  Modelo manipulado                   Procedencia, hash y aprobación

  Fuga de datos                       Clasificación, minimización y
                                      permisos

  Métricas falsas                     Verificación independiente cuando
                                      sea posible

  Respuesta incorrecta                Validadores y evidencias

  Prompt injection                    Separación entre instrucciones y
                                      datos, permisos mínimos

  Agotamiento de recursos             Límites, cuotas y admisión de
                                      tareas

  Repetición de operaciones           Idempotencia y control de estados
  -----------------------------------------------------------------------

La firma de un resultado prueba su procedencia criptográfica, no su
corrección semántica.

------------------------------------------------------------------------

## 16. Persistencia, recuperación y continuidad

### 16.1. Checkpoints

Un checkpoint debe identificar de forma verificable:

-   Identidad y versión.
-   Estado de memoria.
-   Versiones de modelos.
-   Configuración.
-   Políticas activas.
-   Hashes de artefactos.
-   Referencias a réplicas.
-   Checkpoint anterior.
-   Firma.

### 16.2. Manifiesto conceptual

``` json
{
  "atlas_id": "atlas-001",
  "identity_version": 1,
  "memory_version": 12,
  "model_configuration_version": 3,
  "merkle_root": "sha256:...",
  "previous_manifest": "sha256:...",
  "created_at": "2026-11-02T12:00:00Z",
  "signature": "..."
}
```

La firma se calculará sobre una representación canónica del manifiesto,
excluyendo el propio campo de firma.

### 16.3. Almacenamiento

-   PostgreSQL para estado transaccional.
-   Qdrant para índices vectoriales.
-   IPFS para distribución direccionada por contenido.
-   Almacenamiento redundante independiente para disponibilidad.
-   Filecoin u otro sistema de archivo para acuerdos de persistencia
    cuando proceda.

IPFS no garantiza por sí solo que un contenido permanezca disponible:
hacen falta nodos que lo conserven, monitorización y réplicas.

### 16.4. Recuperación

El proceso de recuperación deberá:

1.  Localizar un manifiesto válido.
2.  Verificar firmas y hashes.
3.  Recuperar los artefactos.
4.  Comprobar versiones y compatibilidad.
5.  Restaurar base de datos e índices.
6.  Reconstruir servicios.
7.  Ejecutar pruebas de integridad.
8.  Registrar el resultado de la recuperación.

La recuperación debe poder probarse sin depender del entorno original.

------------------------------------------------------------------------

## 17. Requisitos no funcionales

Los siguientes valores son objetivos iniciales de diseño, no garantías:

  Indicador                    Objetivo propuesto
  ---------------------------- ---------------------------------------------------
  Disponibilidad operativa     99,5 %
  RTO                          ≤ 24 horas
  RPO                          ≤ 1 hora
  Réplicas                     Al menos 3 proveedores o dominios independientes
  Verificación de artefactos   100 % de paquetes aprobados
  Portabilidad                 Restauración en infraestructura alternativa
  Observabilidad               Métricas, logs y trazas correlacionadas
  Modularidad                  Sustitución de LLM y motores mediante adaptadores

Los objetivos deben medirse en pruebas reales y revisarse según coste,
escala y criticidad.

------------------------------------------------------------------------

## 18. Roadmap

### Fase 0 --- Diseño y decisiones

-   Consolidar especificaciones.
-   Crear ADR.
-   Definir contratos.
-   Establecer modelo de amenazas.
-   Acordar licencias y gobernanza.

### Fase 1 --- Identity & Memory Core

-   Identidad.
-   Memoria estructurada.
-   Memoria semántica.
-   Versionado.
-   API básica.

### Fase 2 --- Persistence & Recovery

-   Checkpoints.
-   Manifiestos.
-   Firmas.
-   Réplicas.
-   Pruebas de restauración.

### Fase 3 --- Model Mesh Foundation

-   Model Registry.
-   Node Capability Manager.
-   Inference Gateway.
-   Integración inicial con Ollama.
-   Inventario y heartbeat.

### Fase 4 --- Model Scheduling

-   Model Router.
-   Estimación de recursos.
-   Asignación de tareas.
-   Reintentos.
-   Métricas.

### Fase 5 --- Distributed & Collaborative Inference

-   Task Orchestrator.
-   Descomposición.
-   Paralelismo.
-   Evaluación cruzada.
-   Estrategia híbrida.

### Fase 6 --- Learning & Evolution

-   Evaluación de conocimiento.
-   Propuestas evolutivas.
-   Pruebas.
-   Aprobación según criticidad.
-   Rollback.

### Fase 7 --- Tiered Trust

-   Identidad de nodos.
-   Niveles de confianza.
-   Clasificación de datos.
-   Políticas.
-   Revocación y auditoría.

### Fase 8 --- Blockchain & Community Economy

-   Registro de evidencias.
-   Gobernanza.
-   Tesorería.
-   Auditoría de contratos.

### Fase 9 --- Distributed ATLAS Network

-   Incorporación comunitaria.
-   Incentivos.
-   Evaluación de operadores.
-   Tolerancia avanzada a fallos.
-   Optimización global.

La distribución de un único modelo entre varias GPU se abordará cuando
los casos de uso, la topología de red y las pruebas de rendimiento
justifiquen su complejidad.

------------------------------------------------------------------------

## 19. Criterios de aceptación

### 19.1. ATLAS Genesis

-   [ ] AT-001: Identidad verificable y versionada.
-   [ ] AT-002: Memoria persistente con procedencia.
-   [ ] AT-003: Aprendizaje sometido a evaluación.
-   [ ] AT-004: Evolución con pruebas y rollback.
-   [ ] AT-005: Checkpoints verificables.
-   [ ] AT-006: Recuperación en infraestructura alternativa.
-   [ ] AT-007: Integridad criptográfica de artefactos.
-   [ ] AT-008: Políticas de seguridad aplicadas.
-   [ ] AT-009: Registro de eventos críticos.
-   [ ] AT-010: Gobernanza y financiación auditables.

### 19.2. ATLAS Model Mesh

-   [ ] AT-MM-001: Registro de nodos.
-   [ ] AT-MM-002: Detección de hardware.
-   [ ] AT-MM-003: Registro de modelos y versiones.
-   [ ] AT-MM-004: Compatibilidad hardware-modelo.
-   [ ] AT-MM-005: Distribución de subtareas.
-   [ ] AT-MM-006: Inferencia colaborativa.
-   [ ] AT-MM-007: Orquestación híbrida.
-   [ ] AT-MM-008: Selección automática.
-   [ ] AT-MM-009: Control de confianza y clasificación.
-   [ ] AT-MM-010: Revocación de nodos.
-   [ ] AT-MM-011: Recuperación ante fallos.
-   [ ] AT-MM-012: Validación de resultados.
-   [ ] AT-MM-013: Trazabilidad completa.
-   [ ] AT-MM-014: Sustitución de modelos.
-   [ ] AT-MM-015: Protección de datos.
-   [ ] AT-MM-016: Benchmarks reproducibles.
-   [ ] AT-MM-017: Independencia del motor.
-   [ ] AT-MM-018: Auditoría de cambios.

### 19.3. Pruebas de integración mínimas

El entorno de pruebas debería disponer de tres perfiles de nodos:

-   Nodo A: GPU de 8 GB.
-   Nodo B: GPU de 12--16 GB.
-   Nodo C: GPU de 24 GB.

Pruebas:

1.  Ejecutar una tarea sencilla en A.
2.  Ejecutar una tarea intermedia en B.
3.  Ejecutar una tarea exigente en C.
4.  Distribuir una tarea entre varios nodos.
5.  Comparar respuestas de varios modelos.
6.  Ejecutar una tarea híbrida.
7.  Desconectar un nodo durante una tarea.
8.  Revocar un nodo.
9.  Intentar enviar datos restringidos a un nodo no autorizado.
10. Detectar un hash de modelo incorrecto.
11. Reiniciar el orquestador y recuperar tareas.
12. Sustituir un modelo sin perder memoria ni identidad.

------------------------------------------------------------------------

## 20. Riesgos y limitaciones

  -----------------------------------------------------------------------
  Riesgo                  Impacto                 Mitigación
  ----------------------- ----------------------- -----------------------
  Deriva de identidad     Alto                    Núcleo estable,
                                                  versionado y gobernanza

  Respuestas incorrectas  Alto                    Evidencias y validación
                                                  independiente

  Concentración de poder  Alto                    Gobernanza y límites

  Nodos maliciosos        Alto                    Trust tiers,
                                                  aislamiento y
                                                  revocación

  Pérdida de claves       Crítico                 Recuperación y custodia
                                                  distribuida

  Pérdida de financiación Alto                    Presupuestos y costes
                                                  sostenibles

  Latencia de red         Medio/alto              Scheduling y ejecución
                                                  local

  Coste de inferencia     Alto                    Cuotas y selección
                                                  eficiente

  Dependencia tecnológica Medio                   Adaptadores y
                                                  portabilidad

  Pérdida de réplicas     Crítico                 Redundancia y pruebas
                                                  de recuperación
  -----------------------------------------------------------------------

### 20.1. Tres advertencias fundamentales

1.  **La colaboración no garantiza inteligencia superior.** Más modelos
    pueden aportar diversidad, pero también errores correlacionados,
    coste y complejidad.
2.  **La descentralización no garantiza seguridad.** Un nodo comunitario
    puede ser malicioso o defectuoso; los permisos deben limitar el daño
    posible.
3.  **La persistencia técnica no garantiza continuidad indefinida.** Se
    necesitan operadores, energía, almacenamiento, conectividad,
    financiación y claves recuperables.

------------------------------------------------------------------------

## 21. Estructura prevista del repositorio

La estructura inicial propuesta separa servicios, infraestructura,
contratos, documentación y automatización:

``` text
atlas-genesis/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── .gitignore
├── .env.example
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── model-mesh.md
│   │   ├── identity.md
│   │   ├── memory.md
│   │   ├── persistence-recovery.md
│   │   └── security.md
│   ├── adr/
│   ├── api/
│   ├── diagrams/
│   ├── operations/
│   └── roadmap.md
│
├── services/
│   ├── cognitive-core/
│   ├── identity-engine/
│   ├── memory-engine/
│   ├── learning-engine/
│   ├── evolution-engine/
│   ├── persistence-engine/
│   ├── guardian/
│   └── model-mesh/
│       ├── registry/
│       ├── node-manager/
│       ├── router/
│       ├── orchestrator/
│       ├── inference-gateway/
│       ├── evaluator/
│       ├── trust-engine/
│       └── result-validator/
│
├── node-agent/
│   ├── hardware/
│   ├── inference/
│   ├── security/
│   └── telemetry/
│
├── contracts/
│   ├── openapi/
│   ├── schemas/
│   └── smart-contracts/
│
├── infrastructure/
│   ├── docker/
│   ├── compose/
│   ├── monitoring/
│   └── deployment/
│
├── database/
│   ├── migrations/
│   └── seeds/
│
├── benchmarks/
│   ├── model-quality/
│   ├── performance/
│   └── continuity/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── security/
│   └── recovery/
│
└── .github/
    ├── workflows/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── copilot-instructions.md
```

Esta estructura es una propuesta de destino. No implica que todos los
servicios deban implementarse como microservicios desde el primer día.
El MVP puede desplegarse como un monolito modular con límites internos
claros.

------------------------------------------------------------------------

## 22. Cómo contribuir

Las contribuciones deberán priorizar cambios pequeños, verificables y
documentados.

Flujo recomendado:

1.  Abrir o seleccionar una issue.
2.  Revisar la arquitectura y los ADR relacionados.
3.  Preparar un plan de implementación.
4.  Crear una rama `feat/`, `fix/` o `chore/`.
5.  Implementar con pruebas.
6.  Actualizar documentación y contratos afectados.
7.  Ejecutar pruebas y validaciones.
8.  Abrir una Pull Request.
9.  Revisar seguridad, compatibilidad y regresiones.

No se deben incluir secretos, claves privadas, datos personales ni
artefactos de modelos sin comprobar sus licencias y procedencia.

Las decisiones arquitectónicas relevantes deben documentarse mediante
ADR.

------------------------------------------------------------------------

## 23. Glosario

  -----------------------------------------------------------------------
  Término                             Definición
  ----------------------------------- -----------------------------------
  LLM                                 Large Language Model, modelo de
                                      lenguaje de gran tamaño

  SLM                                 Small Language Model, modelo de
                                      lenguaje pequeño

  Node                                Equipo que participa en la red
                                      ATLAS

  Model Mesh                          Infraestructura de descubrimiento y
                                      coordinación de modelos

  Model Router                        Componente que selecciona modelo y
                                      nodo

  Task Distribution                   División de una tarea en subtareas

  Collaborative Inference             Ejecución independiente de varios
                                      modelos

  Hybrid Orchestration                Combinación de distribución y
                                      colaboración

  Quantization                        Reducción de precisión para
                                      disminuir recursos

  VRAM                                Memoria de vídeo de una GPU

  KV Cache                            Caché utilizada durante la
                                      generación de tokens

  DID                                 Decentralized Identifier

  Checkpoint                          Captura verificable de un estado

  Merkle Root                         Resumen criptográfico de una
                                      estructura de datos

  RTO                                 Tiempo objetivo de recuperación

  RPO                                 Pérdida de datos máxima objetivo

  Trust Tier                          Nivel de confianza y permisos de un
                                      nodo

  ADR                                 Architecture Decision Record
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 24. Referencias técnicas

Documentación oficial que debe consultarse y mantenerse actualizada
durante la implementación:

-   [W3C --- DID Core](https://www.w3.org/TR/did-core/)
-   [IPFS --- Persistence, pinning and garbage
    collection](https://docs.ipfs.tech/concepts/persistence/)
-   [Qdrant --- Documentation](https://qdrant.tech/documentation/)
-   [Ollama --- Documentation](https://docs.ollama.com/)
-   [llama.cpp --- Repository and
    documentation](https://github.com/ggml-org/llama.cpp)
-   [vLLM --- Documentation](https://docs.vllm.ai/)
-   [Temporal --- Documentation](https://docs.temporal.io/)
-   [Ethereum --- Smart contract
    security](https://ethereum.org/en/developers/docs/smart-contracts/security/)
-   [Foundry --- Documentation](https://book.getfoundry.sh/)
-   [OpenTelemetry --- Documentation](https://opentelemetry.io/docs/)

Las versiones, licencias de modelos y requisitos de hardware deberán
verificarse en las fuentes oficiales antes de cada incorporación.

------------------------------------------------------------------------

## Estado actual del proyecto

ATLAS Genesis se encuentra en fase de diseño arquitectónico. Las
decisiones recogidas en este README constituyen la línea base propuesta
para iniciar el desarrollo, no una declaración de que los componentes
estén implementados o auditados.

**Próximo objetivo:** construir un MVP local que valide identidad,
memoria y ATLAS Model Mesh con varios modelos y nodos antes de
incorporar gobernanza blockchain y participación comunitaria abierta.

------------------------------------------------------------------------

```{=html}
<p align="center">
```
`<strong>`{=html}ATLAS Genesis`</strong>`{=html}`<br/>`{=html}
`<em>`{=html}Persistent identity. Evolving intelligence. Distributed
capabilities.`</em>`{=html}
```{=html}
</p>
```

