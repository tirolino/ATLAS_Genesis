# ADR-0006: Identidad operativa y continuidad ante cambio de modelo

Estado: Propuesto

## Contexto
La clave criptográfica y el DID no impiden que cambiar de modelo altere el comportamiento (tono, adherencia a restricciones, planificación). El README no define 'identidad' de forma medible.

## Decisión
Identidad = clave + constitución firmada (reglas nucleares inyectadas a todo modelo) + memoria aceptada. La continuidad se mide con `benchmarks/continuity`: un modelo solo se aprueba si supera los casos must_pass y el umbral del resto. Elección de DID (did:key / did:web) pendiente.

## Consecuencias
Define un criterio objetivo para sustituir modelos. Exige mantener y versionar la suite golden.
