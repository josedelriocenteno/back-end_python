# json_lectura.py
# ==========================
# Lectura de datos JSON en Python usando json.load() y json.loads()
# Explicación detallada y buenas prácticas paso a paso

import json
from pathlib import Path

# ---------------------------------------------------------
# 1️⃣ Qué es JSON
# ---------------------------------------------------------
# JSON (JavaScript Object Notation) es un formato de datos ligero y legible,
# usado para intercambio de información entre sistemas.
# Ejemplo de JSON:
# {
#     "nombre": "Juan",
#     "edad": 30,
#     "hobbies": ["futbol", "lectura"]
# }

# En Python, JSON se convierte automáticamente en dicts, listas, strings, números, bools y None

# ---------------------------------------------------------
# 2️⃣ Leer JSON desde un archivo con json.load()
# ---------------------------------------------------------
# Paso 1: Crear un archivo de ejemplo
ruta_archivo = Path("ejemplo.json")
if not ruta_archivo.exists():
    ruta_archivo.write_text(
        '{"nombre": "Juan", "edad": 30, "hobbies": ["futbol", "lectura"]}',
        encoding="utf-8"
    )

# Paso 2: Abrir archivo y cargar JSON
with open(ruta_archivo, "r", encoding="utf-8") as f:
    datos = json.load(f)  # json.load convierte el JSON en objetos Python
    print("Datos leídos desde archivo:", datos)

# Ahora datos es un diccionario de Python
print("Tipo de datos:", type(datos))
print("Nombre:", datos["nombre"])
print("Edad:", datos["edad"])
print("Primer hobby:", datos["hobbies"][0])

# ---------------------------------------------------------
# 3️⃣ Leer JSON desde un string con json.loads()
# ---------------------------------------------------------
json_string = '{"ciudad": "Madrid", "poblacion": 3223000}'
datos_string = json.loads(json_string)  # Convierte string JSON a dict
print("\nDatos leídos desde string:", datos_string)
print("Ciudad:", datos_string["ciudad"])

# ---------------------------------------------------------
# 4️⃣ Validación básica de estructura
# ---------------------------------------------------------
# Es buena práctica validar que las claves que necesitamos existen
# antes de usarlas, para evitar KeyError

def validar_usuario(data: dict):
    required_keys = ["nombre", "edad", "hobbies"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Falta clave obligatoria: {key}")
    return True

try:
    validar_usuario(datos)
    print("\nJSON validado correctamente")
except ValueError as e:
    print("Error de validación:", e)

# ---------------------------------------------------------
# 5️⃣ Manejo de errores comunes
# ---------------------------------------------------------
# JSON mal formado → json.JSONDecodeError
mal_json = '{"nombre": "Juan", "edad": 30'  # falta cierre
try:
    json.loads(mal_json)
except json.JSONDecodeError as e:
    print("Error al decodificar JSON:", e)

# Archivo inexistente → FileNotFoundError
ruta_inexistente = Path("no_existe.json")
try:
    with open(ruta_inexistente, "r", encoding="utf-8") as f:
        json.load(f)
except FileNotFoundError as e:
    print("Archivo no encontrado:", e)

# ---------------------------------------------------------
# 6️⃣ Buenas prácticas profesionales
# ---------------------------------------------------------
# ✅ Usar encoding="utf-8" siempre
# ✅ Validar estructura del JSON antes de usarlo
# ✅ Manejar json.JSONDecodeError para archivos externos
# ✅ No asumir que claves existen → evitar KeyError
# ✅ Preferir pathlib.Path para manejar rutas
# ✅ Mantener JSON bien indentado y legible para humanos

# ---------------------------------------------------------
# ✅ Conclusión
# ---------------------------------------------------------
# - json.load() → desde archivo
# - json.loads() → desde string
# - Siempre validar y manejar errores
# - Usar pathlib y encoding explícito para portabilidad y seguridad
