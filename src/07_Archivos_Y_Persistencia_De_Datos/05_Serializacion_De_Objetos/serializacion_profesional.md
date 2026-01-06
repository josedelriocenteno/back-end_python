Serialización profesional en Python
Cuándo usar qué (y por qué)
1. Qué es serializar (definición real, no de libro)

Serializar es el proceso de convertir datos que viven en memoria (RAM) en un formato que pueda:

Guardarse en disco

Enviarse por red

Recuperarse más tarde

Leerse por otro programa (o incluso otro lenguaje)

📌 Idea clave:

La memoria muere cuando el programa termina.
La serialización hace que los datos sobrevivan.

2. El error típico de principiante (y por qué es grave)

Muchos juniors piensan:

“Quiero guardar este objeto → uso pickle y listo”

Eso es un error de diseño, no solo técnico.

Porque mezclan dos cosas distintas:

Datos (estado)

Comportamiento (clases, métodos, lógica)

En sistemas profesionales:

Se serializan DATOS

NO se serializa lógica

3. La pregunta correcta antes de serializar

Antes de elegir formato, SIEMPRE responde esto:

¿Quién va a leer estos datos?

El mismo programa

Otro servicio

Un humano

Otro lenguaje

¿Cuánto tiempo deben durar?

Temporal (cache)

Largo plazo (meses / años)

¿Qué volumen tienen?

Pequeño

Grande

Muy grande (GB / TB)

¿Qué pasa si se corrompen?

Nada grave

Error crítico

📌 El formato se elige por contexto, no por comodidad

4. JSON – El estándar universal
Qué es

Formato de texto estructurado, legible por humanos y máquinas.

Cuándo usar JSON

✔ Configuración
✔ APIs (requests / responses)
✔ Datos pequeños y medianos
✔ Persistencia simple
✔ Intercambio entre lenguajes

Ventajas

Seguro (no ejecuta código)

Portable

Fácil de debuggear

Estándar industrial

Limitaciones

No soporta objetos complejos directamente

Más pesado que binario

No ideal para datasets grandes

📌 Regla profesional:

Si dudas, usa JSON

5. CSV – Datos tabulares simples
Qué es

Texto plano con filas y columnas.

Cuándo usar CSV

✔ Datos tabulares simples
✔ Export/import rápido
✔ Compatibilidad con Excel
✔ Data exploration inicial

Ventajas

Ultra simple

Universal

Fácil de generar

Limitaciones

No hay tipos fuertes

No hay jerarquías

Frágil ante cambios de estructura

📌 CSV es para datos, no para estructuras complejas.

6. Pickle – El arma peligrosa
Qué es

Serialización binaria específica de Python que guarda objetos completos.

Cuándo usar pickle (POCAS veces)

⚠️ Entorno 100% controlado
⚠️ Cache local temporal
⚠️ Experimentos rápidos
⚠️ Nunca datos externos

Riesgos reales

❌ Ejecuta código al deserializar
❌ Vulnerable a ataques
❌ No portable
❌ Puede romperse entre versiones

📌 Regla absoluta:

Nunca cargues un pickle que no hayas creado tú mismo

En backend serio:
➡️ pickle está prohibido

7. MsgPack – JSON binario
Qué es

Formato binario eficiente, similar a JSON pero más rápido y compacto.

Cuándo usar MsgPack

✔ Sistemas internos
✔ Cache
✔ Comunicación entre servicios
✔ Alto rendimiento

Ventajas

Seguro

Compacto

Rápido

Limitaciones

No legible

Menos estándar que JSON

📌 Es JSON para cuando el rendimiento importa

8. Parquet – Datos grandes de verdad
Qué es

Formato columnar binario optimizado para analítica.

Cuándo usar Parquet

✔ Data Science
✔ Machine Learning
✔ Big Data
✔ Pipelines reproducibles

Ventajas

Ultra eficiente

Compresión por columnas

Integración con pandas / Spark

Limitaciones

No es para datos pequeños

No es para configuración

📌 Parquet es para datasets, no para apps pequeñas.

9. YAML / INI – Configuración humana
Cuándo usar

✔ Configuración editable
✔ DevOps
✔ Settings de proyectos

Advertencia

YAML mal usado puede ser confuso

Nunca para grandes volúmenes de datos

10. El patrón profesional definitivo

Este patrón nunca falla:

Objeto en memoria
        ↓
    dict / list
        ↓
Formato seguro (JSON / MsgPack / Parquet)
        ↓
      Disco / Red


Y al leer:

Formato
   ↓
dict / list
   ↓
Objeto reconstruido explícitamente


📌 Nada mágico
📌 Todo explícito
📌 Todo controlado

11. Tabla mental rápida (decisión inmediata)
Caso	Formato
Configuración	JSON / YAML
API	JSON
Datos tabulares simples	CSV
Cache rápida	MsgPack
ML / Data	Parquet
Objetos Python internos	Pickle (con miedo)
12. Frase que debes recordar siempre

La serialización no es un detalle técnico.
Es una decisión de arquitectura.

Si eliges mal:

Bugs

Inseguridad

Datos corruptos

Sistemas frágiles

Si eliges bien:

Código limpio

Sistemas robustos

Pipelines reproducibles

Confianza en producción