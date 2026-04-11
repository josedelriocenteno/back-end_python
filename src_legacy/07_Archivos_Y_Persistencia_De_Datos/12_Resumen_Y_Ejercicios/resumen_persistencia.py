"""
resumen_persistencia.py
=======================

Unidad completa de Archivos y Persistencia de Datos.

Objetivo:
---------
Repasar y consolidar todo lo aprendido sobre cómo manejar, almacenar y
proteger datos en Python de manera segura, eficiente y profesional.
"""

import os
import json
import csv
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import pickle

# -----------------------------------------------------------
# 1️⃣ Archivos básicos
# -----------------------------------------------------------
"""
- `open()`, modos: 'r', 'w', 'a', 'rb', 'wb', 'x', etc.
- Leer: read(), readline(), readlines()
- Escribir: write(), writelines()
- Context manager (`with`) asegura cierre automático
"""

ruta_ejemplo = Path("archivo_ejemplo.txt")

# Escritura segura
with open(ruta_ejemplo, "w", encoding="utf-8") as f:
    f.write("Primera línea\nSegunda línea")

# Lectura
with open(ruta_ejemplo, "r", encoding="utf-8") as f:
    lineas = f.readlines()
    print(lineas)

# -----------------------------------------------------------
# 2️⃣ Rutas y sistema de archivos
# -----------------------------------------------------------
"""
- `os.path` y `pathlib.Path` para portabilidad
- `Path.resolve()` para rutas absolutas
- Validar rutas para evitar path traversal
"""

base_dir = Path("/tmp/proyecto_seguro")
archivo_seguro = (base_dir / "datos.txt").resolve()

# Crear directorios si no existen
archivo_seguro.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------
# 3️⃣ JSON
# -----------------------------------------------------------
data = {"nombre": "Juan", "edad": 30}

# Serializar
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Leer
with open("data.json", "r", encoding="utf-8") as f:
    data_leida = json.load(f)

print(data_leida)

# -----------------------------------------------------------
# 4️⃣ CSV
# -----------------------------------------------------------
# Escritura
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["nombre", "edad"])
    writer.writerow(["Ana", 25])

# Lectura con DictReader
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        print(fila)

# -----------------------------------------------------------
# 5️⃣ Archivos temporales
# -----------------------------------------------------------
"""
- `tempfile.NamedTemporaryFile` y `TemporaryDirectory`
- Context managers garantizan limpieza automática
- Evitar nombres fijos y permisos inseguros
"""

with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
    tmp.write("Datos temporales")
    tmp.seek(0)
    print(tmp.read())

# -----------------------------------------------------------
# 6️⃣ Serialización de objetos
# -----------------------------------------------------------
obj = {"clave": "valor"}

# Pickle (no seguro para datos externos)
with open("obj.pickle", "wb") as f:
    pickle.dump(obj, f)

with open("obj.pickle", "rb") as f:
    obj_recuperado = pickle.load(f)
    print(obj_recuperado)

# Alternativas seguras: JSON, msgpack

# -----------------------------------------------------------
# 7️⃣ Archivos de configuración y secretos
# -----------------------------------------------------------
# Variables de entorno (.env)
load_dotenv()  # carga archivo .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Archivos sensibles nunca en texto plano
print(f"Usuario DB: {db_user}")  # No mostrar contraseña

# -----------------------------------------------------------
# 8️⃣ Buenas prácticas resumidas
# -----------------------------------------------------------
"""
1. Siempre usar context managers para leer/escribir archivos.
2. Validar rutas absolutas y restringir acceso a directorios seguros.
3. Usar Pathlib para portabilidad y claridad.
4. Archivos temporales deben limpiarse automáticamente.
5. Datos sensibles → variables de entorno o cifrado.
6. Pickle solo para datos de confianza, usar JSON/Msgpack para portabilidad.
7. Estructurar directorios y archivos para que sea mantenible y reproducible.
8. Logging de archivos: no loguear datos sensibles.
9. Para proyectos grandes, versionado de archivos y datasets es crucial.
"""

# -----------------------------------------------------------
# 9️⃣ Ejemplo integrado
# -----------------------------------------------------------
def procesar_datos():
    """
    Ejemplo de flujo completo:
    - Crear archivo seguro
    - Guardar JSON
    - Procesar CSV temporal
    """
    # Archivo seguro
    secure_path = base_dir / "usuarios.json"
    secure_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar JSON
    usuarios = [{"nombre": "Carlos", "edad": 40}, {"nombre": "Lucia", "edad": 35}]
    with open(secure_path, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2)
    
    # Procesamiento temporal
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp_csv:
        writer = csv.DictWriter(tmp_csv, fieldnames=["nombre", "edad"])
        writer.writeheader()
        for u in usuarios:
            writer.writerow(u)
        tmp_csv.seek(0)
        print("CSV temporal:")
        print(tmp_csv.read())

procesar_datos()
