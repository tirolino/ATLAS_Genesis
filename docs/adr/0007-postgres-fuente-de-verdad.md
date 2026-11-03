# ADR-0007: PostgreSQL como única fuente de verdad en el MVP

Estado: Propuesto

## Contexto
El README lista PostgreSQL, Qdrant, NATS/Redis, Temporal e IPFS desde el inicio; cada pieza añade operación y puntos de fallo.

## Decisión
PostgreSQL (+pgvector) para estado, auditoría y embeddings. Qdrant, colas y workflows durables detrás de puertos y solo cuando una medición lo justifique. Backups verificados desde la Fase 2.

## Consecuencias
Una sola pieza que operar. Un único Postgres es punto único de fallo hasta que existan réplicas y restauración probada.
