-- =============================================================================
-- SQL PROFESIONAL: EJERCICIOS DE MODELADO Y QUERIES
-- CASOS REALES DE BACKEND Y DATA ENGINEERING
-- =============================================================================

/*
EJERCICIO 1: MODELADO DE UNA PLATAFORMA DE E-LEARNING
-----------------------------------------------------------------------------
Requisitos:
- Usuarios (estudiantes y profesores).
- Cursos (pertenecen a una categoría, creados por un profesor).
- Inscripciones (un estudiante puede estar en muchos cursos).
- Lecciones (cada curso tiene N lecciones).

OBJETIVO:
1. Diseña las tablas con PKs y FKs correctas.
2. Usa UUIDs.
3. Asegura que un estudiante no se inscriba dos veces al mismo curso.
*/

-- TU SOLUCIÓN AQUÍ...


/*
EJERCICIO 2: CONSULTA DE ANALÍTICA (WINDOW FUNCTIONS)
-----------------------------------------------------------------------------
Usando una tabla hipotética 'orders' (id, user_id, amount, created_at):

OBJETIVO:
Obtén un listado de todos los pedidos que incluya:
1. El ID de la orden.
2. El ID del usuario.
3. El monto de la orden.
4. El monto total que ese usuario ha gastado hasta ese momento (Running Total).
5. Cuánto representó esa orden sobre el total gastado de ese usuario (%).
*/

-- TU SOLUCIÓN AQUÍ...


/*
EJERCICIO 3: OPTIMIZACIÓN Y EXPLAIN
-----------------------------------------------------------------------------
Tienes la siguiente query que tarda 5 segundos en ejecutarse:
`SELECT * FROM logs WHERE level = 'error' AND created_at > '2023-01-01';`

OBJETIVO:
1. Escribe el comando para ver el plan de ejecución.
2. Propón el índice que creas que acelerará más esta consulta.
*/

-- TU SOLUCIÓN AQUÍ...


/*
EJERCICIO 4: JSONB Y PYTHON
-----------------------------------------------------------------------------
Tienes una tabla 'products' con una columna 'metadata' JSONB.
Dentro de metadata hay un campo 'specs' que contiene 'color' y 'weight'.

OBJETIVO:
Escribe la query para encontrar todos los productos cuyo color sea 'Space Gray'
y pesen menos de 1.5kg.
*/

-- TU SOLUCIÓN AQUÍ...


-- =============================================================================
-- SOLUCIONES SUGERIDAS (No mires hasta terminar)
-- =============================================================================

/*
SOLUCIÓN 1 (Resumen):
- Tablas: roles, users, categories, courses, lessons, enrollments.
- CONSTRAINT unique_enrollment UNIQUE(user_id, course_id).

SOLUCIÓN 2:
SELECT 
    id, user_id, amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at) as running_total,
    (amount / SUM(amount) OVER (PARTITION BY user_id)) * 100 as percent_of_total
FROM orders;

SOLUCIÓN 4:
SELECT * FROM products 
WHERE metadata @> '{"specs": {"color": "Space Gray"}}'
  AND (metadata->'specs'->>'weight')::numeric < 1.5;
*/
