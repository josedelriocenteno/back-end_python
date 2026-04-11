# pickle_basico.py
# ==========================
# Serialización de objetos Python con pickle
# Permite guardar objetos en disco y recuperarlos más tarde
# Útil para persistencia rápida de datos o modelos pequeños

import pickle
from pathlib import Path

# ---------------------------------------------------------
# 1️⃣ Qué es la serialización
# ---------------------------------------------------------
# Serializar = convertir un objeto en una secuencia de bytes
# para poder:
#   - Guardarlo en un archivo
#   - Enviarlo por la red
#   - Persistirlo entre ejecuciones del programa
#
# Deserializar = reconstruir el objeto original desde los bytes

# Ejemplo conceptual:
objeto = {"nombre": "Juan", "edad": 30, "hobbies": ["futbol", "lectura"]}
print("Objeto original:", objeto)

# ---------------------------------------------------------
# 2️⃣ Guardar objeto en archivo (serialización)
# ---------------------------------------------------------
ruta_pickle = Path("usuario.pkl")

# Abrir archivo en modo binario escritura ('wb')
with ruta_pickle.open("wb") as f:
    pickle.dump(objeto, f)  # Convierte objeto a bytes y lo guarda

print(f"Objeto serializado en: {ruta_pickle}")

# ---------------------------------------------------------
# 3️⃣ Recuperar objeto del archivo (deserialización)
# ---------------------------------------------------------
with ruta_pickle.open("rb") as f:  # 'rb' = lectura binaria
    objeto_cargado = pickle.load(f)

print("Objeto deserializado:", objeto_cargado)

# Verificación
assert objeto == objeto_cargado, "Error: el objeto recuperado difiere del original"

# ---------------------------------------------------------
# 4️⃣ Serializar múltiples objetos
# ---------------------------------------------------------
usuarios = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Luis", "edad": 28},
]

ruta_pickle_usuarios = Path("usuarios.pkl")
with ruta_pickle_usuarios.open("wb") as f:
    pickle.dump(usuarios, f)

with ruta_pickle_usuarios.open("rb") as f:
    usuarios_cargados = pickle.load(f)

print("Usuarios cargados:", usuarios_cargados)

# ---------------------------------------------------------
# 5️⃣ Buenas prácticas y advertencias
# ---------------------------------------------------------
# ✅ Serializar objetos simples: dict, list, set, tuple, clases simples
# ✅ Versionar archivos pickle si los objetos cambian de estructura
# ❌ Nunca cargar pickle de fuentes no confiables (riesgo de ejecución de código malicioso)
# ✅ Para intercambio seguro, considerar JSON u otros formatos
# ✅ Mantener consistencia de encoding y rutas
# ✅ Documentar qué objetos se serializan y para qué
# ✅ Evitar usar pickle para almacenamiento a largo plazo de datos críticos
# ✅ Usar pickle solo dentro de entornos controlados

# ---------------------------------------------------------
# 6️⃣ Resumen
# ---------------------------------------------------------
# - pickle.dump() → serializa un objeto a un archivo binario
# - pickle.load() → deserializa un objeto desde archivo
# - Ideal para persistencia rápida de prototipos o modelos ligeros
# - Riesgo: seguridad y compatibilidad entre versiones de Python
# - Alternativa segura: JSON, msgpack, Parquet (para datos tabulares)

print("✅ Serialización con pickle completada")
