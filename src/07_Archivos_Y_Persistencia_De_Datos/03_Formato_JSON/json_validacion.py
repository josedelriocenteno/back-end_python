# json_validacion.py
# ==========================
# Validación de estructuras JSON en Python
# Cómo asegurarse de que los datos que recibimos cumplen con lo esperado
# Evitar errores de tipo y claves faltantes

import json
from pathlib import Path
from typing import Any, Dict, List

# ---------------------------------------------------------
# 1️⃣ Ejemplo de JSON esperado
# ---------------------------------------------------------
# Supongamos que recibimos este JSON de un archivo o API
json_data = """
{
    "nombre": "Luis",
    "edad": 28,
    "hobbies": ["futbol", "lectura"],
    "activo": true
}
"""

# Convertimos a objeto Python
try:
    datos: Dict[str, Any] = json.loads(json_data)
except json.JSONDecodeError as e:
    raise ValueError(f"JSON mal formado: {e}")

# ---------------------------------------------------------
# 2️⃣ Validación manual paso a paso
# ---------------------------------------------------------
# Queremos asegurarnos de que las claves obligatorias existen
# y que cada clave tenga el tipo esperado

def validar_usuario(usuario: Dict[str, Any]) -> bool:
    # Claves obligatorias y tipos esperados
    esquema = {
        "nombre": str,
        "edad": int,
        "hobbies": list,
        "activo": bool
    }
    
    for clave, tipo in esquema.items():
        if clave not in usuario:
            raise ValueError(f"Falta clave obligatoria: {clave}")
        if not isinstance(usuario[clave], tipo):
            raise TypeError(f"Clave '{clave}' debe ser {tipo.__name__}, "
                            f"pero es {type(usuario[clave]).__name__}")
    
    return True

# Validamos el JSON recibido
try:
    if validar_usuario(datos):
        print("JSON validado correctamente:", datos)
except (ValueError, TypeError) as e:
    print("Error de validación:", e)

# ---------------------------------------------------------
# 3️⃣ Validación de listas de objetos
# ---------------------------------------------------------
# Si tenemos una lista de usuarios
json_lista = """
[
    {"nombre": "Ana", "edad": 25, "hobbies": ["pintura"], "activo": true},
    {"nombre": "Carlos", "edad": "30", "hobbies": ["tenis"], "activo": false}
]
"""
datos_lista = json.loads(json_lista)

for i, usuario in enumerate(datos_lista):
    try:
        validar_usuario(usuario)
        print(f"Usuario {i} validado correctamente")
    except (ValueError, TypeError) as e:
        print(f"Error en usuario {i}:", e)

# ---------------------------------------------------------
# 4️⃣ Buenas prácticas profesionales
# ---------------------------------------------------------
# ✅ Definir claramente la estructura esperada del JSON
# ✅ Validar:
#    - Claves obligatorias
#    - Tipos de datos
#    - Listas y subobjetos
# ✅ Capturar y reportar errores claros (ValueError / TypeError)
# ✅ Validar antes de usar los datos para evitar fallos posteriores
# ✅ Para estructuras complejas, considerar librerías como:
#    - pydantic
#    - marshmallow
#    - cerberus

# ---------------------------------------------------------
# 5️⃣ Resumen
# ---------------------------------------------------------
# Validación JSON profesional:
# 1. Parsear el JSON con json.load() o json.loads()
# 2. Definir un esquema esperado (claves + tipos)
# 3. Recorrer y validar cada clave y tipo
# 4. Capturar y manejar errores explícitamente
# 5. Para listas, iterar y validar cada elemento
# 6. Considerar librerías de validación para proyectos grandes

print("✅ Validación de JSON completada con éxito")
