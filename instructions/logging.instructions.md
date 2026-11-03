---
applyTo: "**/*.py"
---

# Logging y diagnóstico

- Usa `logging.getLogger(__name__)`; configura handlers y formato en el punto de entrada o configuración central.
- Registra eventos significativos, cambios de estado, duración de operaciones importantes y fallos.
- Incluye contexto como `execution_id`, `correlation_id` y nombre de operación cuando aporte valor.
- Usa `logger.exception()` dentro de un bloque `except` cuando se necesite el traceback.
- Evita registrar de nuevo la misma excepción en cada capa.
- No registres contraseñas, tokens, secretos, cookies ni datos personales sensibles.
- No uses `print()` para diagnóstico.
- Usa niveles DEBUG, INFO, WARNING, ERROR y CRITICAL con significado consistente.
- No añadas logs a cada función trivial: prioriza señales útiles y evita ruido.
- La configuración debe permitir nivel, destino, formato y retención adecuados al entorno.
