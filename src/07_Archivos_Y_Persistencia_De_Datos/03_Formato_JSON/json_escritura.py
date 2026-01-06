# json_escritura.py
# ==========================
# Escritura de datos JSON en Python usando json.dump() y json.dumps()
# Explicación detallada y buenas prácticas paso a paso

import json
from pathlib import Path

# ---------------------------------------------------------
# 1️⃣ Datos de ejemplo
# ---------------------------------------------------------
# Creamos un diccionario de Python que queremos guardar como JSON
usuario = {
    "nombre": "Ana",
    "edad": 25,
    "hobbies": ["pintura", "guitarra", "lectura"],
    "activo": True
}

# ---------------------------------------------------------
# 2️⃣ Escribir JSON en un archivo con json.dump()
# ---------------------------------------------------------
ruta_archivo = Path("usuario.json")

# Abrimos el archivo en modo escritura ('w') y especificamos UTF-8
with ruta_archivo.open("w", encoding="utf-8") as f:
    # json.dump escribe el diccionario en el archivo como JSON
    # indent=4 → hace el JSON legible (sangría de 4 espacios)
    # ensure_ascii=False → permite caracteres Unicode
    json.dump(usuario, f, indent=4, ensure_ascii=False)

print(f"Datos escritos en archivo JSON: {ruta_archivo}")

# ---------------------------------------------------------
# 3️⃣ Escribir JSON a un string con json.dumps()
# ---------------------------------------------------------
# json.dumps convierte dict/list a string JSON
json_string = json.dumps(usuario, indent=4, ensure_ascii=False)
print("\nJSON como string:\n", json_string)

# Útil para enviar datos en APIs, logs o almacenamiento temporal

# ---------------------------------------------------------
# 4️⃣ Buenas prácticas al escribir JSON
# ---------------------------------------------------------
# ✅ Usar UTF-8 para compatibilidad
# ✅ Indentar para legibilidad cuando el archivo será leído por humanos
# ✅ ensure_ascii=False para soportar caracteres especiales
# ✅ Validar los datos antes de escribir (tipos correctos: dict, list, str, int, float, bool, None)
# ✅ Manejar excepciones si escribimos en disco

try:
    ruta_error = Path("/ruta/que/no/existe/archivo.json")
    with ruta_error.open("w", encoding="utf-8") as f:
        json.dump(usuario, f, indent=4)
except FileNotFoundError as e:
    print("Error al escribir JSON:", e)

# ---------------------------------------------------------
# 5️⃣ Comparación dump() vs dumps()
# ---------------------------------------------------------
# json.dump() → escribe directamente en un archivo
# json.dumps() → devuelve string JSON, no escribe en disco

# Ejemplo práctico:
# Enviar JSON a una API → usar dumps()
# Guardar JSON local → usar dump()

# ---------------------------------------------------------
# 6️⃣ Resumen profesional
# ---------------------------------------------------------
# - json.dump(obj, file, indent=4, ensure_ascii=False) → archivo
# - json.dumps(obj, indent=4, ensure_ascii=False) → string
# - Usar pathlib para rutas
# - Siempre UTF-8
# - Manejar errores de escritura
# - Validar los datos antes de serializar

print("\n✅ JSON escrito correctamente con buenas prácticas")
