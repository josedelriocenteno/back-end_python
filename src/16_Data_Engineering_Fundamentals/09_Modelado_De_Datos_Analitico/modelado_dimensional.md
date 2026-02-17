# Modelado Dimensional: La base del BI

El modelado dimensional es una técnica de diseño de bases de datos que busca que las consultas de negocio sean rápidas, intuitivas y fáciles de usar por personas que no son expertas en SQL.

## 1. Hechos y Dimensiones: Los dos pilares
- **Hechos (Facts):** Registran eventos cuantitativos o métricas. Representan "qué pasó". (Ej: Una venta, un click, un login).
- **Dimensiones:** Registran el contexto cualitativo de los hechos. Responden a "Quién, Dónde, Cuándo, Cómo". (Ej: Cliente, Producto, Tienda, Tiempo).

## 2. La Regla de la Escala
- Las tablas de **Hechos** crecen muy rápido (millones de filas al día). Son tablas estrechas pero muy largas.
- Las tablas de **Dimensiones** crecen despacio. Son tablas anchas (muchas columnas con descripciones) pero cortas.

## 3. Claves Subrogadas (Surrogate Keys)
En modelado dimensional, no usamos el ID que viene de la App (ej: UUID de la App) como clave primaria. Creamos un entero secuencial (`1, 2, 3...`) propio del Warehouse.
- **Por qué:** Independencia de la fuente original y mejor rendimiento en los `JOINs`.

## 4. Medidas Aditivas, Semi-aditivas y No Aditivas
- **Aditivas:** Se pueden sumar en todas las dimensiones (ej: Ventas).
- **Semi-aditivas:** Solo se pueden sumar en algunas (ej: Saldo bancario; no puedes sumar el saldo de ayer y hoy para saber cuánto tienes hoy).
- **No Aditivas:** Ratios o porcentajes (ej: % de margen).

## 5. El Granularidad (Grain)
Define qué representa una sola fila en la tabla de hechos. 
- **Ejemplo:** "Una fila por cada producto en cada pedido". 
- Es fundamental que todos los registros de una tabla tengan la misma granularidad.

## Resumen: Diseñar para la Consulta
El modelado dimensional no busca ahorrar espacio (como el modelo normalizado de Backend), busca **ahorrar tiempo mental** al analista. Una base de datos dimensional debe ser auto-explicativa.
