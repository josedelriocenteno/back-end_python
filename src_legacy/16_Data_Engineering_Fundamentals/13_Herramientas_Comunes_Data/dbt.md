# dbt (data build tool): El SQL como ingeniería

**dbt** ha revolucionado el mundo de la analítica de datos al aplicar las mejores prácticas de la ingeniería de software (Git, Tests, Documentación) al mundo del SQL.

## 1. El paradigma de dbt
"Nosotros no movemos datos, nosotros transformamos los que ya están en el Warehouse". dbt está diseñado para el modelo **ELT**. Tú escribes un `SELECT` y dbt se encarga de crear la tabla o vista en la base de datos.

## 2. Ref() y Dependencias
En dbt no escribes nombres de tablas fijos como `FROM raw_data.orders`. Escribes `FROM {{ ref('orders') }}`.
- dbt construye automáticamente el grafo de dependencias y sabe qué tabla debe procesar primero.

## 3. Tests de Datos Integrados
dbt permite validar tus datos con una línea de configuración. Puedes asegurar que una columna nunca sea nula o que los IDs sean únicos. Si el test falla, dbt te avisa antes de que el dato llegue al reporte.

## 4. Documentación Automática
Con un solo comando (`dbt docs generate`), dbt analiza tu código y genera una web con descripciones de tablas, columnas y un mapa visual de cómo fluye el dato (Linaje).

## 5. Modificadores (Macros) y Jinja
dbt permite usar lógica de programación dentro de SQL (bucles, condicionales) usando el motor de plantillas **Jinja**. Esto permite crear código SQL reutilizable y dinámico.

## Resumen: SQL de Alto Nivel
dbt ha convertido al analista de datos en un "Analytics Engineer". Permite que equipos enteros colaboren sobre el mismo código SQL con la misma seguridad y rigor que un equipo de desarrolladores de Backend.
