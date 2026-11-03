# ADR-0003: Salidas del LLM estructuradas y fail-closed

Estado: Propuesto

## Contexto
Un LLM devuelve texto probabilístico; si el núcleo interpreta texto libre para decidir, cualquier variación o inyección puede disparar acciones.

## Decisión
El Cognitive Core solo acepta JSON conforme a un esquema (`DECISION_SCHEMA`), usando salida estructurada del motor cuando exista y validación estricta propia siempre. Sin reparaciones ni tolerancia a markdown. Herramientas en lista blanca.

## Consecuencias
Comportamiento predecible y testeable. Validez de esquema no implica corrección: se necesitan validadores semánticos por herramienta.
