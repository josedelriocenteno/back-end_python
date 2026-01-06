Introducción a Parquet
Columnar Storage explicado desde cero (bien)
1. El problema REAL que Parquet viene a resolver

Antes de hablar de Parquet, hay que entender qué problema existe.

Imagina este escenario:

Tienes un dataset con millones de filas

Cada fila tiene muchas columnas:

id

nombre

edad

país

ingresos

fecha

score

etc.

Y quieres hacer algo muy común en Data / ML:

“Dame SOLO la columna ingresos de todos los registros”

Aquí es donde los formatos clásicos fallan.

2. Cómo se almacenan los datos normalmente (row-based)
CSV, JSON, bases de datos simples → row-based

Eso significa:

Fila 1 → todas sus columnas
Fila 2 → todas sus columnas
Fila 3 → todas sus columnas
...


Visualmente:

[id, nombre, edad, país, ingresos]
[id, nombre, edad, país, ingresos]
[id, nombre, edad, país, ingresos]

Problema

Si solo quieres ingresos:

El sistema lee TODO

Luego descarta lo que no necesita

Mucha lectura de disco innecesaria

Muy lento con datasets grandes

📌 El disco es miles de veces más lento que la RAM

3. Qué es almacenamiento columnar (columnar storage)

En columnar storage, los datos se guardan por columnas, no por filas.

Visualmente:

id:        [1, 2, 3, 4, ...]
nombre:    ["A", "B", "C", ...]
edad:      [20, 21, 22, ...]
ingresos:  [30000, 32000, 31000, ...]


Cada columna vive junta.

4. Por qué esto es brutalmente eficiente
Caso real

Quieres:

media de ingresos

Con columnar storage:

Solo se lee la columna ingresos

No se toca nada más

Menos I/O

Menos RAM

Mucho más rápido

📌 Esto es clave en ML y Big Data

5. Qué es Parquet exactamente

Apache Parquet es:

Un formato binario

Columnar

Optimizado para:

Lectura selectiva

Compresión

Analítica

ML

No es un formato “general”
👉 es especializado

6. Por qué Parquet comprime tan bien

Porque las columnas tienen datos homogéneos.

Ejemplo:

edad = [20, 21, 22, 23, 24, 25]


Esto se comprime muchísimo mejor que:

[20, "Juan", "España", 30000, ...]


📌 Columnas homogéneas = compresión brutal

7. Qué NO es Parquet (esto es importante)

❌ No es legible por humanos
❌ No es para configuración
❌ No es para logs
❌ No es para datos pequeños
❌ No es para editar a mano

Parquet es para:

máquinas leyendo datos, no personas

8. Cuándo usar Parquet (reglas claras)

Usa Parquet cuando:

✔ Tienes datasets grandes
✔ Usas pandas, Spark, Dask
✔ Trabajas en ML / Data Science
✔ Quieres reproducibilidad
✔ Necesitas velocidad
✔ El schema es estable

9. Cuándo NO usar Parquet

No lo uses cuando:

❌ Dataset pequeño
❌ Necesitas editar manualmente
❌ Proyecto simple
❌ Configuración
❌ APIs

Para eso:
➡️ JSON / CSV

10. Parquet en el ecosistema Data / ML

Parquet es estándar en:

Pandas

Spark

Hadoop

AWS Athena

BigQuery

Databricks

ML pipelines profesionales

📌 Saber Parquet no es opcional en Data / ML serio

11. Parquet y reproducibilidad (muy importante)

En ML necesitas:

Mismos datos

Mismo orden

Mismo schema

Parquet:
✔ mantiene tipos
✔ mantiene columnas
✔ reduce errores silenciosos

CSV:
❌ todo es texto
❌ errores invisibles

12. Resumen mental definitivo

Guárdate esto:

CSV / JSON → humanos
Parquet → máquinas

Row-based → apps
Columnar → analítica

13. Frase clave que debes memorizar

Parquet no hace tu código más bonito.
Hace tus pipelines posibles.