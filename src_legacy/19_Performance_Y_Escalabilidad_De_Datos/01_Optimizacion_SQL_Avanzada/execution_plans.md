# Planes de Ejecución: El Mapa de la Query

Para optimizar una base de datos, no puedes adivinar. Tienes que preguntar a la base de datos cómo está ejecutando tu consulta. Esto se hace mediante los **Planes de Ejecución**.

## 1. El comando EXPLAIN
`EXPLAIN` te dice el "plan de batalla" que el optimizador ha decidido seguir ANTES de ejecutar la query.
```sql
EXPLAIN SELECT * FROM usuarios WHERE email = 'test@example.com';
```

## 2. EXPLAIN ANALYZE (La Verdad)
Mientras que `EXPLAIN` hace una estimación, `EXPLAIN ANALYZE` **ejecuta la query real** y mide el tiempo exacto.
> [!WARNING]
> Ten cuidado al usar `EXPLAIN ANALYZE` con `DELETE` o `UPDATE` en producción, ¡porque borrará los datos de verdad!

## 3. Conceptos Clave en un Plan
*   **Seq Scan (Sequential Scan):** La base de datos lee TODA la tabla fila por fila. Es lento en tablas grandes. Suele significar que falta un índice.
*   **Index Scan:** Usa un índice para encontrar los datos directamente. Es muy rápido.
*   **Cost:** Un número arbitrario que estima el esfuerzo. `(cost=0.00..12.50)`. El primer número es el tiempo para empezar, el segundo para terminar.
*   **Actual Time:** El tiempo real medido en milisegundos.

## 4. Tipos de Operaciones comunes
*   **Filter:** Se descartan filas basándose en una condición `WHERE`.
*   **Sort:** Ordenar los datos (`ORDER BY`). Si ocurre en disco (External Merge Sort), es un gran cuello de botella.
*   **Hash Join / Nested Loop:** Cómo se están uniendo dos tablas.

## 5. El "Checklist" de Optimización
1.  **Busca Sequential Scans** en tablas grandes. ¿Puedes añadir un índice?
2.  **Mira las estimaciones de filas (rows).** Si la base de datos estima 1 fila pero llegan 1 millón, las estadísticas están desactualizadas (Usa `ANALYZE` para refrescarlas).
3.  **Verifica los Sorts.** ¿Puedes usar un índice para que los datos ya vengan ordenados?

## Resumen: No vueles a ciegas
Aprender a leer un `EXPLAIN` es lo que separa a un desarrollador de un Ingeniero de Datos Senior. Es la herramienta definitiva para identificar por qué una base de datos va lenta y cómo arreglarla científicamente.
