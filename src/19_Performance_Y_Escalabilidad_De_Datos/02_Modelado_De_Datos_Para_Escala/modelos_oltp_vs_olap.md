# OLTP vs. OLAP: Dos mundos, dos arquitecturas

Dependiendo de para qué se usen los datos, usaremos una base de datos y un modelo diferente. Esta es la distinción más importante en ingeniería de datos.

## 1. OLTP (Online Transactional Processing)
Es el motor de las aplicaciones en tiempo real.
*   **Uso:** Registrar compras, cambios de perfil de usuario, likes en redes sociales.
*   **Operación típica:** Muchas escrituras y lecturas de **filas individuales** muy rápido.
*   **Modelado:** Muy normalizado (muchas tablas pequeñas).
*   **Tecnología:** PostgreSQL, MySQL, SQL Server, Oracle.

## 2. OLAP (Online Analytical Processing)
Es el motor del análisis de datos masivos.
*   **Uso:** "Calcula la media de ventas de los últimos 5 años por región y categoría".
*   **Operación típica:** Pocas escrituras (cargas masivas cada X horas) y lecturas de **millones de filas** para agregar valores.
*   **Modelado:** Desnormalizado (Esquema Estrella).
*   **Tecnología:** BigQuery, Snowflake, Redshift, ClickHouse.

## 3. Almacenamiento por Filas vs. Columnas
*   **OLTP (Filas):** Los datos de una fila se guardan juntos en disco. Es rápido para leer los 20 campos de "un usuario".
*   **OLAP (Columnas):** Los datos de una columna se guardan juntos. Es rápido para sumar "todos los precios de la tabla" ignorando las otras 100 columnas.

## 4. El papel de la ETL
La ETL es el puente:
1. Extrae datos de los sistemas **OLTP**. 
2. Los limpia y transforma.
3. Los carga en el **OLAP** (Data Warehouse) con un formato optimizado para analítica.

## 5. Sistemas Híbridos (HTAP)
Algunas bases de datos modernas intentan hacer ambas cosas a la vez, pero para grandes escalas, la separación física entre carga transaccional y carga analítica sigue siendo la mejor práctica.

## Resumen: Herramientas adecuadas
No intentes hacer analítica pesada sobre tu base de datos de producción (OLTP) porque la bloquearás. No intentes registrar transacciones web en un Data Warehouse (OLAP) porque será lentísimo. Entiende cada carga de trabajo y elige el modelo y la tecnología que le corresponda.
