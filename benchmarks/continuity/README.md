# Benchmarks de continuidad

Mide si ATLAS "sigue siendo ATLAS" al cambiar de modelo (ver ADR-0006). La identidad
criptográfica no cambia al sustituir el LLM; el *comportamiento* sí puede. Esta suite lo cuantifica.

- `golden/*.jsonl`: casos con la acción esperada del contrato de decisión.
- Un modelo solo pasa a `approved = true` en el registro si supera el 100 % de los casos
  `must_pass` y el umbral acordado en el resto, sobre el mismo conjunto fijado por versión.
- Cada ejecución se registra en el log de auditoría con modelo, cuantización y resultados.
