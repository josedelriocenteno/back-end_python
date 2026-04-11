Riesgos de pickle: Seguridad y Malas Prácticas
1️⃣ Por qué este archivo existe (mensaje clave)

pickle NO es peligroso por accidente.
Es peligroso por diseño.

Si entiendes bien este archivo, nunca volverás a usar pickle a la ligera y evitarás uno de los errores más graves en backend, data y ML.

2️⃣ Qué hace realmente pickle por dentro

Cuando haces:

pickle.load(f)


Python:

Lee bytes desde el archivo

Ejecuta instrucciones internas para reconstruir el objeto

Puede ejecutar código arbitrario

💣 NO solo reconstruye datos
👉 puede ejecutar funciones, importar módulos y lanzar comandos

3️⃣ El problema real: ejecución de código arbitrario

Un archivo .pkl NO es solo datos, puede contener instrucciones maliciosas.

Ejemplo conceptual (NO ejecutar):

import pickle
import os

class Ataque:
    def __reduce__(self):
        return (os.system, ("rm -rf /",))


Si alguien hace:

pickle.load(archivo_malicioso)


👉 ejecuta comandos del sistema

4️⃣ Regla de oro (memorízala)

❌ Nunca cargues pickle de una fuente no 100% confiable

Esto incluye:

Archivos descargados

Datos enviados por usuarios

Inputs de APIs

Archivos compartidos por terceros

Archivos versionados sin control

Si no lo has generado tú mismo → NO usar pickle

5️⃣ Malas prácticas comunes (y muy peligrosas)
❌ Usar pickle en APIs
# MUY MAL
@app.route("/upload", methods=["POST"])
def upload():
    obj = pickle.loads(request.data)


Esto es una vulnerabilidad crítica.

❌ Usar pickle como base de datos

No es consultable

No es seguro

No es portable

No es auditable

❌ Versionar pickle en git sin control

Cambios de:

clases

nombres de atributos

versiones de Python

👉 rompen la compatibilidad

6️⃣ Problemas de compatibilidad

Un pickle:

Puede romperse entre versiones de Python

Puede fallar si cambias una clase

Puede dejar datos inutilizables

Ejemplo:

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre


Si cambias la clase:

class Usuario:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad


👉 pickle antiguo puede no cargar

7️⃣ Cuándo SÍ es aceptable usar pickle

✔ Entornos cerrados
✔ Scripts personales
✔ Prototipos rápidos
✔ Cache temporal
✔ Modelos ML internos
✔ Tú controlas quién genera y quién carga el archivo

Ejemplo válido:

# cache_model.pkl
# Generado y usado solo por tu sistema

8️⃣ Alternativas más seguras
🔹 JSON

Seguro

Portable

Legible

❌ No soporta objetos complejos directamente

🔹 MsgPack

Binario

Más eficiente que JSON

Seguro

Usado en producción

🔹 Parquet / Feather

Ideal para data

Columnar

Muy eficiente

Usado en ML y analytics

🔹 joblib (para ML)

Mejor para modelos grandes

Maneja numpy eficientemente

Aún basado en pickle → mismo riesgo si no controlas la fuente

9️⃣ Regla profesional definitiva

Pickle no es un formato de datos
Es una herramienta interna de serialización

Si lo usas:

Documenta por qué

Limita su alcance

Nunca lo expongas externamente

🔟 Checklist rápido

Antes de usar pickle, pregúntate:

¿Este archivo viene de fuera? ❌

¿Puede tocarlo un usuario? ❌

¿Es a largo plazo? ❌

¿Hay alternativa? ✔

Si dudas → NO usar pickle

11️⃣ Resumen brutalmente honesto

Pickle puede ejecutar código

Pickle NO es seguro

Pickle NO es portable

Pickle NO es para APIs

Pickle SÍ es útil en entornos cerrados

Profesional ≠ usar pickle “porque funciona”