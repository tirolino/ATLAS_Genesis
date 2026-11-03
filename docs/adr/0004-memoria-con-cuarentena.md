# ADR-0004: Memoria con cuarentena y transiciones controladas

Estado: Propuesto

## Contexto
El Learning Engine podría ingerir resultados de nodos comunitarios; sin barrera hay riesgo de envenenamiento persistente de la memoria y de los índices vectoriales.

## Decisión
Estados RECEIVED→QUARANTINED→VALIDATED→ACCEPTED (+REJECTED/REVOKED). Un LLM no valida ni acepta. Fuentes T0/T1 solo se aceptan por un humano o un validador determinista con evidencia. Los embeddings son derivados y solo de memorias ACCEPTED.

## Consecuencias
Más fricción al aprender, a cambio de integridad. Revocar una memoria exige reconstruir índices.
