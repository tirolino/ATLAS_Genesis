# ADR-0005: Alcance de estrategias del Mesh en el MVP

Estado: Propuesto

## Contexto
HYBRID/COLLABORATIVE multiplican latencia (manda el nodo más lento) y coste (el juez puede ser mayor que los modelos evaluados), y los errores de modelos similares están correlacionados.

## Decisión
MVP: SINGLE con selección por filtros duros (confianza, clase de datos, aprobación, capacidades, contexto, VRAM estimada) y calidad medida. DISTRIBUTED por pipeline en Fase 3. COLLABORATIVE/HYBRID solo con evidencia de ganancia; preferir validadores deterministas (tests, esquemas, ejecución) a un LLM juez. Las demás estrategias lanzan UnsupportedStrategy.

## Consecuencias
Menos superficie y coste. Se conserva el enum y el modelo de datos para no rediseñar después.
