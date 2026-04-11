# Almacenamiento OLTP vs. OLAP: Diferencias Técnicas

Entender la diferencia entre sistemas transaccionales (OLTP) y analíticos (OLAP) es fundamental para saber dónde depositar el dato y cómo consultarlo.

## 1. OLTP (Online Transactional Processing)
- **Misión:** Registrar transacciones individuales al instante.
- **Estructura:** Modelos muy normalizados (muchas tablas pequeñas unidas por IDs). Esto evita la redundancia.
- **Operaciones:** Millones de `INSERT`, `UPDATE` y `DELETE` por segundo de registros únicos.
- **Ejemplo:** Tu banco registrando una transferencia.

## 2. OLAP (Online Analytical Processing)
- **Misión:** Analizar tendencias y responder preguntas complejas.
- **Estructura:** Modelos desnormalizados (tablas grandes con mucha información repetida para evitar `JOINs` costosos).
- **Operaciones:** Pocas cargas masivas de datos, millones de `SELECT` que recorren toda la tabla.
- **Ejemplo:** "Dime el total de transferencias de los últimos 5 años agrupado por país y edad del cliente".

## 3. Almacenamiento de Fila vs. Columna
- **OLTP (Fila):** Ideal para cuando necesitas "todos los campos de un usuario". Si buscas por ID de usuario, la base de datos lee una sola línea del disco.
- **OLAP (Columna):** Ideal para cuando necesitas "un campo de todos los usuarios". Si quieres la media de edad, la base de datos salta directamente a la columna de edad e ignora el resto (nombre, email, etc.).

## 4. Cuándo mover datos de uno a otro
Los datos nacen en OLTP (la App). Una vez que la transacción termina, el Data Engineer los mueve al OLAP para que los analistas no saturen la base de datos de la App y para poder hacer consultas que en el OLTP tardarían horas.

## 5. Transacciones vs. Analítica
No intentes usar PostgreSQL como tu warehouse principal si tienes Terabytes de datos. Y no intentes usar BigQuery como la base de datos de tu aplicación móvil. Cada herramienta tiene su propósito.

## Resumen: Herramientas para el trabajo
Diferenciar OLTP de OLAP te permite diseñar arquitecturas que no solo funcionan, sino que escalan. Un Data Engineer Senior sabe que el secreto de la velocidad no es solo el código, sino colocar el dato en el formato de almacenamiento adecuado para su uso final.
