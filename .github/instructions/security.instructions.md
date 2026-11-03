---
description: "Usa al tratar entradas externas, autenticación, secretos, dependencias, red o límites de confianza."
applyTo: "**/*.py"
---

# Seguridad

- Trata toda entrada externa como no confiable y valídala en los límites del sistema.
- No hardcodees secretos ni los incluyas en logs, errores o pruebas.
- Evita `eval`, `exec`, deserialización insegura y comandos shell construidos con datos no confiables.
- Usa timeouts y límites en llamadas externas.
- Aplica mínimo privilegio y maneja archivos temporales de forma segura.
- No desactives verificaciones TLS ni controles de seguridad para resolver errores.
- Revisa nuevas dependencias y vulnerabilidades conocidas.
- No ejecutes operaciones destructivas o contra sistemas reales sin autorización.
