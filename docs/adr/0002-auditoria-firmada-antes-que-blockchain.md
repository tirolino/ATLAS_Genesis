# ADR-0002: Log de auditoría firmado y anclado antes que blockchain

Estado: Propuesto

## Contexto
El README sitúa contratos EVM en la Fase 8. Para el MVP basta con integridad verificable de eventos, pero una cadena de hashes firmada con una sola clave no impide que su dueño reescriba el historial ni detecta truncados.

## Decisión
Log append-only con hash encadenado y firma Ed25519 (`atlas.audit`), hashes canónicos sin floats, y publicación periódica de la cabeza en un medio externo (Git firmado, RFC 3161, testigo). Blockchain solo si se necesita no-equivocación pública o gobernanza multiparte.

## Consecuencias
Menos infraestructura y coste. Hay que implementar y operar el anclaje externo; sin él, solo se detecta manipulación parcial.
