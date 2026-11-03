---
description: "Usa al diseñar o modificar módulos Python, capas, dependencias o límites arquitectónicos."
applyTo: "src/**/*.py"
---

# Arquitectura y modularidad

- Inspecciona primero la estructura y los patrones existentes.
- Mantén alta cohesión, bajo acoplamiento y dependencias dirigidas de forma consistente.
- Separa dominio, aplicación, persistencia e interfaces cuando el tamaño y el dominio lo justifiquen.
- Mantén los efectos externos en límites identificables y sustituibles en pruebas.
- Evita dependencias circulares y lógica de negocio dentro de controladores o puntos de entrada.
- No crees carpetas, clases, interfaces o capas vacías o sin responsabilidad real.
- No muevas código no relacionado con la tarea.
- Documenta decisiones arquitectónicas no obvias y sus alternativas.
