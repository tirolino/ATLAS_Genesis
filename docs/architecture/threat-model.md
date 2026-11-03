# Modelo de amenazas (borrador)

| Activo | Amenaza | Control actual | Pendiente |
|---|---|---|---|
| Claves de identidad | Exfiltración vía LLM/herramientas | Cognitive Core sin acceso a `shared.crypto` | KMS/HSM, rotación, custodia con quórum |
| Memoria aceptada | Envenenamiento / inyección persistente | Cuarentena + reglas de transición | Validadores deterministas reales, escaneo de contenido |
| Prompts de usuario | Fuga a nodos no confiables | Regla D/T en el router, log solo con hashes | Redacción de PII, mTLS entre nodos |
| Registro de auditoría | Reescritura / truncado | Cadena de hashes firmada | Anclaje externo periódico de la cabeza |
| Model Registry | Modelo manipulado | Solo modelos registrados y aprobados | Verificación de hash en el nodo |
| Métricas de nodos | Declaraciones falsas | Tratadas como no verificadas | Benchmarks de reto-respuesta |
| Salida del LLM | Texto libre que dispara acciones | Contrato JSON fail-closed | Validación semántica por herramienta |
| Privacidad en nodos | El nodo ve el prompt en claro | D2/D3 solo a T3 (hardware propio) | Inferencia confidencial si llega a ser viable |
