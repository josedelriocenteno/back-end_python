# Esquema Copo de Nieve (Snowflake Schema)

El esquema copo de nieve es una variación del esquema estrella donde las tablas de dimensiones están **normalizadas**, dividiéndose en tablas secundarias.

## 1. La Estructura
Si en la estrella la dimensión Productos incluía la Categoría, en el copo de nieve:
- `fact_sales` se conecta a `dim_products`.
- `dim_products` se conecta a `dim_categories`.
Visualmente, las puntas de la estrella se ramifican, pareciendo un copo de nieve.

## 2. Ventajas
- **Ahorro de Espacio:** Elimina la redundancia de datos.
- **Integridad de Datos:** Es más difícil tener inconsistencias (ej: un error tipográfico en el nombre de una categoría) porque el nombre solo se escribe en un sitio.
- **Mantenimiento:** Actualizar el nombre de una categoría se hace en una sola fila.

## 3. Desventajas (El precio a pagar)
- **Complejidad SQL:** El analista tiene que hacer 3 `JOINs` en lugar de 1 para obtener un reporte básico.
- **Menor Rendimiento:** Cada `JOIN` extra consume recursos y tiempo en sistemas de Big Data.

## 4. Estrella vs. Copo de Nieve
| Característica | Estrella | Copo de Nieve |
| :--- | :--- | :--- |
| **Normalización** | Desnormalizado | Normalizado |
| **Facilidad de Uso** | Muy Alta | Media |
| **Rendimiento Query** | Mayor | Menor |
| **Mantenimiento** | Más difícil | Más fácil |

## 5. Cuándo usar Copo de Nieve
Hoy en día, con el bajo coste del almacenamiento y la potencia de herramientas como BigQuery, el Copo de Nieve ha perdido popularidad frente a la Estrella. Sin embargo, sigue siendo útil si tienes dimensiones con millones de registros que cambian constantemente.

## Resumen: ¿Pureza o Practicidad?
El copo de nieve es técnicamente más "puro" desde el punto de vista de las bases de datos, pero el esquema estrella es más práctico para el análisis de negocio. Como Data Engineer, tu tendencia debe ser siempre hacia la estrella a menos que la normalización sea estrictamente necesaria.
