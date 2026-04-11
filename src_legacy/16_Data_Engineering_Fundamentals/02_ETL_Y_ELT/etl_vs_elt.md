# ETL vs. ELT: ¿Cuál elegir?

La forma en que mueves y transformas los datos ha evolucionado drásticamente con la llegada de la nube. Entender la diferencia es clave para diseñar arquitecturas eficientes.

## 1. ETL (Extract, Transform, Load)
El patrón tradicional. Los datos se transforman **antes** de llegar al destino final.
- **Flujo:** Extraer -> Servidor de Procesamiento (Spark/Python) -> Transformar -> Cargar al Warehouse.
- **Cuándo usar:** 
  - Cuando el destino tiene poca potencia de cálculo.
  - Cuando los datos crudos contienen información sensible (PII) que debe eliminarse antes de guardarse.
  - Cuando los datos son masivos y no quieres pagar por guardarlos crudos.

## 2. ELT (Extract, Load, Transform)
El estándar moderno. Los datos se cargan "crudos" y se transforman **dentro** del almacén de datos.
- **Flujo:** Extraer -> Cargar al Warehouse (BigQuery/Snowflake) -> Transformar (SQL).
- **Cuándo usar:**
  - En la mayoría de proyectos modernos en la nube.
  - Cuando quieres mantener la "historia cruda" por si en el futuro necesitas re-procesarla de forma diferente.
  - Cuando tu equipo domina SQL mejor que Python/Spark.

## 3. Comparativa Técnica
| Característica | ETL | ELT |
| :--- | :--- | :--- |
| **Velocidad de Carga** | Lenta (espera a la transf.) | Muy Rápida |
| **Flexibilidad** | Baja (esquema rígido inicial) | Alta (transformas según necesites) |
| **Coste** | Más caro en cómputo externo | Más caro en almacenamiento |
| **Mantenimiento** | Complejo (scripts de código) | Simple (vistas y tablas SQL) |

## 4. El auge del ELT y dbt
ELT se ha popularizado gracias a herramientas como **dbt**, que permite gestionar las transformaciones dentro del Data Warehouse como si fueran proyectos de ingeniería de software, con tests y documentación.

## 5. El enfoque híbrido
Muchas empresas usan ETL para la ingesta inicial (limpiar nulos básicos, tipos) y luego ELT para la lógica de negocio compleja.

## Resumen: Potencia en el Destino
ETL es para cuando el destino es débil. ELT es para cuando el destino (la nube) es infinitamente escalable. En 2024, si puedes elegir, intenta moverte hacia **ELT**.
