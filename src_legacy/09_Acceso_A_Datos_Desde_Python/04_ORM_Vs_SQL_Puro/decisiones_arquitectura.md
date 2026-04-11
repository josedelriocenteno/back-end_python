# Decisiones de Arquitectura: ¿Cuándo saltar del ORM?

Un arquitecto de Backend debe saber cuándo la abstracción del ORM se convierte en un lastre en lugar de una ayuda. Estos son los indicadores clave (Red Flags).

## 1. El Indicador de Complejidad (The Joins Rule)
Si tu consulta requiere unir más de 5 o 6 tablas con filtros complejos y subqueries:
*   **ORM:** El código se vuelve una maraña de funciones anidadas difíciles de seguir.
*   **Acción:** Escribe una **Vista (View)** en SQL y mapea el ORM a la vista, o usa SQL puro.

## 2. El Indicador de Rendimiento
Si una ruta de tu API tarda más de 500ms y el `EXPLAIN ANALYZE` muestra que la query es buena, pero el ORM tarda 300ms en "hidratar" los objetos:
*   **ORM:** La transformación de filas de la DB a objetos Python es costosa.
*   **Acción:** Usa SQLAlchemy Core para obtener diccionarios/tuplas directamente.

## 3. El Indicador de Migraciones
Si necesitas cambiar un tipo de datos en una tabla de 100 millones de filas sin Downtime:
*   **ORM:** Las migraciones automáticas pueden ser peligrosas.
*   **Acción:** Escribe el SQL manual de la migración (`ALTER TABLE ... CONCURRENTLY`) e ignora el autogenerador del ORM.

## 4. La Regla de Oro: Persistencia Políglota
No tienes por qué elegir uno para todo el proyecto.
*   **Escrituras (Commands):** El ORM es genial para validar y guardar cambios en un solo registro.
*   **Lecturas (Queries):** SQL puro o Core es mejor para reportes y listados complejos.
*   *Este patrón se conoce como **CQRS** (Command Query Responsibility Segregation).*

## 5. Mantenibilidad a Largo Plazo
Los strings de SQL en el código son difíciles de refactorizar (si cambias el nombre de una columna, el IDE no te avisa).
*   **Estrategia:** Centraliza tus queries de SQL puro en una capa de Repositorios para que sean fáciles de localizar y actualizar.

## Resumen: Pragmatismo sobre Dogmatismo

No seas un purista del ORM ni un hater de las abstracciones. Un backend moderno y escalable usa el ORM para la mayoría de sus tareas transaccionales y recurre al SQL táctico cuando la escala o la complejidad lo exigen.
