# Buenas Prácticas de Modelado: El decálogo del Data Engineer

Un buen modelo de datos es como una buena obra de ingeniería: robusto, elegante y construido para durar años.

## 1. Nombra con Sentido
- Tablas de hechos: `fact_nombre` (o `fct_`).
- Tablas de dimensiones: `dim_nombre`.
- Sé consistente: Si usas `created_at` en una tabla, no uses `creation_date` en otra.

## 2. No a los IDs Naturales
Evita usar el email o el DNI como clave primaria en el Warehouse. Si el usuario cambia de email, tu integridad referencial se rompe. Usa siempre **Claves Subrogadas** (Surrogate Keys).

## 3. La tabla de Tiempo (Dim Calendar)
Nunca dependas de las funciones de fecha nativas de SQL para todo. Crea una tabla `dim_calendar` con una fila por día que ya tenga pre-calculado el trimestre, si es festivo, el nombre del mes, etc. Ahorrarás miles de horas de cálculo y errores.

## 4. No guardes "Nulos" en las Claves Foráneas
Si un pedido no tiene cliente asignado:
- **MAL:** Poner `NULL` en `customer_id`.
- **BIEN:** Poner `-1` y tener una fila en `dim_customers` con ID `-1` y nombre `"Cliente Desconocido"`. Esto permite hacer `INNER JOINS` seguros sin perder filas.

## 5. Desnormaliza con Sabiduría
Repetir el nombre del producto es bueno. Repetir un documento PDF entero en cada fila es un desastre. Desnormaliza solo los campos descriptivos que se usan en los filtros de los reportes.

## 6. Documenta el Linaje
Usa herramientas que permitan ver de qué tabla `raw` viene cada tabla `fact`. Un modelo indocumentado muere el día que el ingeniero que lo hizo se va de la empresa.

## Resumen: Calidad desde el Diseño
El modelado no es "dibujar tablas". Es entender el negocio y plasmarlo en una estructura técnica que soporte el crecimiento de la compañía. Dedica tiempo a pensar antes de empezar a escribir código de pipeline.
