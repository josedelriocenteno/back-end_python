# Subqueries vs. CTE: Legibilidad y Rendimiento

¿Qué es mejor? ¿Una subconsulta dentro de un `WHERE` o una **Common Table Expression (CTE)** con el comando `WITH`? La respuesta depende de la base de datos y de la complejidad de la lógica.

## 1. Subqueries (Subconsultas)
Son consultas dentro de otras consultas.
```sql
SELECT nombre FROM usuarios 
WHERE id IN (SELECT usuario_id FROM pedidos WHERE total > 100);
```
*   **Pros:** Estándar, soportado por todos.
*   **Contras:** Difícil de leer si se anidan muchas. A veces el optimizador las trata de forma ineficiente si no están "correlacionadas".

## 2. CTE (WITH Queries)
Permiten definir un "conjunto de resultados temporal" al inicio de la query.
```sql
WITH pedidos_grandes AS (
    SELECT usuario_id FROM pedidos WHERE total > 100
)
SELECT u.nombre FROM usuarios u
JOIN pedidos_grandes pg ON u.id = pg.usuario_id;
```
*   **Pros:** Mucho más legibles. Permiten consultas recursivas (vital para jerarquías o árboles).
*   **Contras:** En versiones antiguas de PostgreSQL, las CTE eran "vallas de optimización" (el motor las ejecutaba por separado sin poder optimizar la query global).

## 3. ¿Cuál rinde más?
En los motores modernos (PostgreSQL 12+, SQL Server, BigQuery), **el rendimiento suele ser idéntico**. El optimizador es capaz de "desenrollar" la CTE e integrarla en la query principal.

## 4. Cuándo usar cada una
*   **Usa CTE si:** La lógica es compleja, necesitas reutilizar el mismo trozo de datos varias veces en la misma query, o necesitas recursividad.
*   **Usa Subqueries si:** Es un filtro muy simple y directo que no aporta complejidad visual.

## 5. El peligro de las CTEs enormes
Si tu CTE genera 10 millones de filas para luego filtrar 9.9 millones en la query final, podrías estar desperdiciando recursos. Intenta siempre filtrar los datos **dentro de la propia CTE** para que el set de datos intermedio sea lo más pequeño posible.

## Resumen: Claridad es Poder
El rendimiento es importante, pero la mantenibilidad también. Las CTEs han ganado la batalla de la legibilidad. Usa `WITH` para que tus compañeros (y tu "yo del futuro") entiendan qué hace la query, y confía en el optimizador moderno para que el rendimiento sea óptimo.
