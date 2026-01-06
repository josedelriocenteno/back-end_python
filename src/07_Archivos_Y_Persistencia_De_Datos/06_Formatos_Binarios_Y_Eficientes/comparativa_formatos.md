Comparativa de formatos de datos
CSV vs JSON vs Parquet (cuándo usar cada uno de verdad)
1. El error más común al empezar

La mayoría de gente piensa:

“Todos los formatos guardan datos, así que da igual”

Esto es falso.

Elegir mal el formato:

hace tu código lento

rompe pipelines

crea bugs invisibles

te obliga a rehacer todo después

📌 El formato es una decisión de arquitectura, no de comodidad.

2. Antes de comparar: ¿qué es un formato de datos?

Un formato de datos define:

Cómo se escriben los datos en disco

Cómo se leen en memoria

Qué información de tipos se conserva

Qué tan rápido es

Qué tan grande ocupa

Quién lo puede leer (humanos vs máquinas)

3. CSV — el formato más malentendido
Qué es CSV

CSV = Comma Separated Values

Ejemplo:

id,edad,pais,ingresos
1,25,ES,30000
2,32,ES,45000


Es texto plano.

Ventajas reales de CSV

✔ Muy simple
✔ Editable a mano
✔ Compatible con todo
✔ Fácil de aprender

Problemas reales de CSV

❌ Todo es texto
❌ No hay tipos reales
❌ Errores silenciosos
❌ Muy lento con grandes volúmenes
❌ No soporta columnas selectivas
❌ Archivos grandes en disco

Ejemplo de bug silencioso:

"30000" vs "30.000"


👉 nadie te avisa

Cuándo usar CSV (reglas claras)

✔ Datasets pequeños
✔ Intercambio rápido
✔ Prototipos
✔ Datos humanos

Cuándo NO usar CSV

❌ ML serio
❌ Producción
❌ Pipelines grandes
❌ Datos críticos

4. JSON — estructurado pero no eficiente
Qué es JSON

JSON = JavaScript Object Notation

Ejemplo:

{
  "id": 1,
  "edad": 25,
  "pais": "ES",
  "ingresos": 30000
}


Es texto estructurado.

Ventajas reales de JSON

✔ Estructura clara
✔ Ideal para APIs
✔ Autodescriptivo
✔ Muy usado en backend

Problemas reales de JSON

❌ Muy verboso
❌ Poco eficiente
❌ Tipos limitados
❌ Repetición de claves
❌ Lento con grandes volúmenes

JSON repite:

"id", "edad", "pais", "ingresos"


en cada registro.

Cuándo usar JSON

✔ APIs
✔ Configuración
✔ Payloads
✔ Comunicación entre servicios

Cuándo NO usar JSON

❌ Datasets grandes
❌ Analítica
❌ ML
❌ Almacenamiento masivo

5. Parquet — diseñado para máquinas
Qué es Parquet

Parquet es:

Binario

Columnar

Optimizado

Tipado

Compacto

No es para humanos.

Ventajas reales de Parquet

✔ Lectura por columnas
✔ Compresión excelente
✔ Tipos fuertes
✔ Muy rápido
✔ Ideal para ML
✔ Escala a Big Data

Problemas reales de Parquet

❌ No editable
❌ Curva de aprendizaje
❌ Requiere librerías
❌ No sirve para config

Cuándo usar Parquet

✔ ML
✔ Data Science
✔ Pipelines grandes
✔ Producción
✔ Analítica

6. Comparativa directa (tabla mental)
Criterio	CSV	JSON	Parquet
Legible por humanos	✔	✔	❌
Tipos reales	❌	Parcial	✔
Tamaño en disco	Grande	Muy grande	Pequeño
Velocidad	Lento	Lento	Muy rápido
Columnas selectivas	❌	❌	✔
ML / Big Data	❌	❌	✔
7. El criterio profesional (memoriza esto)

Formato ≠ gusto personal
Formato = contexto

Pregunta siempre:

¿Quién lee los datos?

¿Cuántos datos?

¿Con qué frecuencia?

¿Con qué finalidad?

8. Ejemplo real de decisión correcta
Proyecto ML

Raw data → CSV (ingesta inicial)

Procesado → Parquet

Features → Parquet

Modelos → binario

Config → JSON / YAML

9. Error típico de juniors

“Uso CSV porque es más fácil”

Eso funciona:

el día 1

el día 2

El día 30:
💥 todo lento
💥 bugs
💥 refactor masivo

10. Frase que debes grabarte

CSV y JSON son para personas.
Parquet es para sistemas.

11. Conexión con tu roadmap (importante)

Tú quieres:

Backend serio

Data / ML

Reproducibilidad

👉 Parquet no es opcional para ti.