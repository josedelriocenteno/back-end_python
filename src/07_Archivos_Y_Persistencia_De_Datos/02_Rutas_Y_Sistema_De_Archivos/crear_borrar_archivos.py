# crear_borrar_archivos.py
# ==========================
# Crear y borrar archivos y carpetas en Python
# Uso de os y pathlib, paso a paso, explicado profesionalmente

import os
from pathlib import Path

# ---------------------------------------------------------
# 1️⃣ Crear carpetas
# ---------------------------------------------------------
# Usando os.makedirs()
# Crea una carpeta y todas las intermedias si no existen
ruta_carpeta = "proyecto/datos"
os.makedirs(ruta_carpeta, exist_ok=True)  # exist_ok evita error si ya existe
print(f"Carpeta creada (o ya existía): {ruta_carpeta}")

# Usando pathlib.Path.mkdir()
carpeta_pathlib = Path("proyecto/pathlib_datos")
carpeta_pathlib.mkdir(parents=True, exist_ok=True)
print(f"Carpeta creada con Pathlib: {carpeta_pathlib}")

# ---------------------------------------------------------
# 2️⃣ Crear archivos vacíos
# ---------------------------------------------------------
# Usando open() con modo 'w'
archivo = open("proyecto/datos/archivo_vacio.txt", "w", encoding="utf-8")
archivo.close()  # cerramos para guardar
print("Archivo vacío creado: proyecto/datos/archivo_vacio.txt")

# Usando pathlib.Path.touch()
archivo_pathlib = Path("proyecto/pathlib_datos/archivo_touch.txt")
archivo_pathlib.touch(exist_ok=True)  # exist_ok evita error si ya existe
print("Archivo vacío creado con Pathlib:", archivo_pathlib)

# ---------------------------------------------------------
# 3️⃣ Borrar archivos
# ---------------------------------------------------------
# Usando os.remove()
archivo_a_borrar = "proyecto/datos/archivo_vacio.txt"
if os.path.exists(archivo_a_borrar) and os.path.isfile(archivo_a_borrar):
    os.remove(archivo_a_borrar)
    print(f"Archivo borrado: {archivo_a_borrar}")
else:
    print(f"No se puede borrar, archivo no existe: {archivo_a_borrar}")

# Usando pathlib.Path.unlink()
archivo_pathlib.unlink()  # borra archivo_touch.txt
print(f"Archivo borrado con Pathlib: {archivo_pathlib}")

# ---------------------------------------------------------
# 4️⃣ Borrar carpetas
# ---------------------------------------------------------
# Usando os.rmdir() → solo funciona si la carpeta está vacía
ruta_vacia = "proyecto/datos"
if os.path.exists(ruta_vacia) and os.path.isdir(ruta_vacia):
    try:
        os.rmdir(ruta_vacia)
        print(f"Carpeta vacía borrada: {ruta_vacia}")
    except OSError:
        print(f"No se puede borrar, la carpeta no está vacía: {ruta_vacia}")

# Usando pathlib.Path.rmdir()
carpeta_pathlib.rmdir()  # también solo borra vacías
print(f"Carpeta vacía borrada con Pathlib: proyecto/pathlib_datos")

# ---------------------------------------------------------
# 5️⃣ Borrar carpetas con contenido (recursivamente)
# ---------------------------------------------------------
# os → shutil.rmtree()
import shutil

ruta_completa = Path("proyecto")  # carpeta proyecto con subcarpetas
# Solo borrar si realmente queremos eliminar todo
# shutil.rmtree(ruta_completa)

# Nota: Con Pathlib, rmtree sigue siendo con shutil, Pathlib no tiene rmtree

# ---------------------------------------------------------
# 6️⃣ Buenas prácticas
# ---------------------------------------------------------
# ✅ Verificar existencia antes de borrar
# ✅ Diferenciar archivos y carpetas con isfile()/isdir()
# ✅ No usar rmtree sin confirmación → riesgo de pérdida total de datos
# ✅ Para creación de carpetas, usar exist_ok=True
# ✅ Para archivos, touch(exist_ok=True) o open('w') según necesidad

# ---------------------------------------------------------
# 7️⃣ Resumen práctico
# ---------------------------------------------------------
# Crear:
# - os.makedirs(ruta, exist_ok=True)
# - Path(ruta).mkdir(parents=True, exist_ok=True)
# Archivos:
# - open("archivo.txt", "w") → crea vacíos
# - Path("archivo.txt").touch(exist_ok=True)
# Borrar:
# - os.remove() / Path.unlink() → archivos
# - os.rmdir() / Path.rmdir() → carpetas vacías
# - shutil.rmtree() → carpetas con contenido

print("✅ Operaciones de creación y borrado completadas correctamente")
