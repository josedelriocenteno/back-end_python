# Data Warehouse: El templo de la analítica de negocio

Un Data Warehouse (Almacén de Datos) es una base de datos optimizada exclusivamente para la lectura y el análisis masivo de datos estructurados.

## 1. Características Clave
- **Orientado a Temas:** Organizado por áreas de negocio (Ventas, Clientes, Inventario).
- **Integrado:** Homogeneiza datos que vienen de fuentes dispares.
- **No Volátil:** Los datos no se borran ni cambian; se añaden versiones nuevas (histórico).
- **Variante en el Tiempo:** Permite ver la evolución del negocio a lo largo de meses o años.

## 2. Tecnologías Modernas (Cloud Data Warehouse)
- **Google BigQuery:** Serverless, escala automáticamente.
- **Snowflake:** Separación total entre almacenamiento y cómputo.
- **Amazon Redshift:** Basado en clústeres de alto rendimiento.

## 3. Almacenamiento Columnar
Como vimos anteriormente, los Warehouses guardan los datos por columnas. Esto permite que una query que suma las ventas de 1.000 millones de registros responda en segundos, ya que solo lee la columna de importes.

## 4. El fin del ETL tradicional
Con la potencia de los Warehouses modernos, ya no necesitamos transformar los datos fuera. Los cargamos crudos (ELT) y usamos el SQL del propio Warehouse para crear las tablas finales.

## 5. Data Warehouse vs. DB Transaccional (OLTP)
| Característica | Base de Datos (App) | Data Warehouse |
| :--- | :--- | :--- |
| **Uso Principal** | Operaciones diarias (CRUD) | Reportes y Decisiones |
| **Volumen** | Gigabytes | Terabytes / Petabytes |
| **Usuarios** | Millones (clientes) | Cientos (analistas) |
| **Optimización** | Escritura de filas | Lectura de columnas |

## Resumen: La Verdad Oficial
El Data Warehouse es donde vive la "Versión única de la verdad" de la empresa. Es el lugar donde los datos se vuelven oficiales, limpios y accesibles para los que toman las decisiones.
