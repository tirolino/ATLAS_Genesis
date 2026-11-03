# ADR-0001: Monolito modular con fronteras impuestas

Estado: Propuesto

## Contexto
El README propone ~15 servicios. Para un MVP con un solo equipo y pocos nodos, los microservicios añaden red, despliegue y fallos parciales sin aportar valor.

## Decisión
Un único paquete `atlas` con módulos por motor, capas que solo se importan hacia abajo y comprobación con import-linter en CI. Los motores se comunican por puertos (Protocol), de modo que extraer uno a servicio sea mecánico.

## Consecuencias
Despliegue y depuración simples. Riesgo: erosión de fronteras, mitigado por CI. Extraer servicios cuando haya un motivo medible.
