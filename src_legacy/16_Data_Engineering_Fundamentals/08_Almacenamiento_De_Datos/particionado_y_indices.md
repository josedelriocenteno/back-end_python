# Particionado e Índices: Rendimiento Estructural

Cuando manejas miles de millones de filas, un `SELECT *` puede tardar horas. El particionado y el correcto uso de índices (o su equivalente en Big Data) son las herramientas para mantener la velocidad.

## 1. Particionado (Partitioning)
Consiste en dividir físicamente una tabla grande en trozos más pequeños basados en una columna (normalmente la **fecha**).
- **Cómo funciona:** Si particionas por `día`, y pides los datos del 15 de Marzo, el motor de base de datos **solo lee** la carpeta/partición de ese día. Al resto del disco ni lo mira.
- **Beneficio:** Reduce drásticamente el I/O y el coste de la query.

## 2. Clusterización (Clustering) / Índices
Mientras que la partición divide archivos, la clusterización ordena los datos **dentro** de esos archivos.
- Si clusterizas por `user_id`, todos los registros del mismo usuario estarán físicamente juntos en el disco.
- **Beneficio:** Las búsquedas por ese campo son instantáneas.

## 3. Índices en el mundo Big Data
En Big Data (Parquet/Spark) no solemos usar índices tradicionales como en SQL. Usamos:
- **Predicate Pushdown:** El archivo Parquet guarda el MIN y MAX de cada columna en cada trozo. Si buscas `precio > 100` y un trozo dice `max_precio = 50`, el sistema descarta ese trozo sin leerlo.

## 4. Antipatrón: Over-partitioning
Particionar por un campo con demasiados valores distintos (ej: ID de usuario o Hora:Minuto:Segundo).
- **Problema:** Creas miles de archivos minúsculos de pocos KB. El "overhead" de abrir cada archivo hace que la query sea más lenta que si no hubiera partición.

## 5. Estrategia recomendada
1. **Particiona por tiempo** (Día o Mes) casi siempre. Es el eje natural de los datos.
2. **Clusteriza por las columnas** que más uses en tus filtros `WHERE` o en tus uniones `JOIN`.

## Resumen: Ayuda al motor de búsqueda
El particionado es decirle a la base de datos en qué estante buscar. Los índices son decirle en qué posición del estante está el libro. Sin estas técnicas, el Big Data es inmanejable.
