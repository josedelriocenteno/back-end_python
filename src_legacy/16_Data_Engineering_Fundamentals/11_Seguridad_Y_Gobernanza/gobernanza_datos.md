# Gobernanza del Dato (Data Governance)

Si la ingeniería de datos es construir las tuberías, la gobernanza es el reglamento que dice quién puede usarlas y qué calidad de agua debe fluir por ellas.

## 1. ¿Qué es la Gobernanza?
Es el marco de políticas, procesos y estándares para asegurar que los datos del negocio sean precisos, privados y seguros.

## 2. El Catálogo de Datos (Data Catalog)
Es el "Google" de tus datos. Una herramienta donde cualquier analista puede buscar:
- ¿Qué significa la columna `mkt_spend`?
- ¿Quién es el dueño (Owner) de esta tabla?
- ¿Cuál es el linaje (de dónde viene este dato)?
- **Herramientas:** DataHub, Amundsen, Google Data Catalog.

## 3. Diccionario de Datos
Un documento técnico que define cada campo: nombre, tipo, descripción y reglas de negocio asociadas.

## 4. Data Lineage (Trazabilidad)
Es el mapa que une las fuentes con los reportes finales.
- Si un reporte de ventas falla, el linaje te permite ver rápidamente en qué paso del pipeline se corrompió el dato.
- Fundamental para auditorías y para entender el impacto de un cambio en el backend.

## 5. El "Data Steward"
Es una figura (humana) responsable de la calidad y el significado de un conjunto de datos. No es necesariamente un ingeniero, suele ser alguien de negocio que sabe qué reglas debe cumplir el dato para ser útil.

## Resumen: Del Caos al Control
La gobernanza es lo que permite que una empresa escale. Sin ella, el equipo de datos gasta el 50% de su tiempo respondiendo a la pregunta "¿Este dato qué significa?". Con gobernanza, el dato es un activo transparente y confiable.
