# pathlib_basico.py
# ==========================
# Manejo de rutas y archivos en Python usando pathlib
# La forma moderna y profesional de trabajar con rutas
# Paso a paso, explicado sin asumir conocimientos previos

from pathlib import Path  # Importamos la clase Path, núcleo de pathlib

# ---------------------------------------------------------
# 1️⃣ Crear un objeto Path
# ---------------------------------------------------------
# Un Path representa un archivo o carpeta en el sistema
# No es una cadena, sino un objeto con métodos útiles
ruta = Path("mi_carpeta") / "archivo.txt"  # '/' concatena rutas de manera portable
print("Objeto Path:", ruta)
print("Tipo:", type(ruta))  # <class 'pathlib.PosixPath'> o WindowsPath

# ---------------------------------------------------------
# 2️⃣ Comparación con os.path.join()
# ---------------------------------------------------------
# Con os.path.join:
import os
ruta_os = os.path.join("mi_carpeta", "archivo.txt")
print("Ruta con os.path:", ruta_os)

# Path hace lo mismo de manera más intuitiva, con operador '/' y métodos modernos

# ---------------------------------------------------------
# 3️⃣ Verificar existencia y tipo
# ---------------------------------------------------------
if ruta.exists():
    print(f"'{ruta}' existe")
else:
    print(f"'{ruta}' no existe")

if ruta.is_file():
    print(f"'{ruta}' es un archivo")
elif ruta.is_dir():
    print(f"'{ruta}' es un directorio")

# ---------------------------------------------------------
# 4️⃣ Obtener información del Path
# ---------------------------------------------------------
print("Nombre del archivo:", ruta.name)       # archivo.txt
print("Carpeta contenedora:", ruta.parent)   # mi_carpeta
print("Extensión del archivo:", ruta.suffix) # .txt
print("Ruta absoluta:", ruta.resolve())      # ruta completa en el SO

# ---------------------------------------------------------
# 5️⃣ Crear carpetas y archivos
# ---------------------------------------------------------
# Crear carpeta si no existe
nueva_carpeta = Path("nueva_carpeta")
nueva_carpeta.mkdir(exist_ok=True)  # exist_ok=True evita error si ya existe

# Crear un archivo vacío
archivo_vacio = nueva_carpeta / "archivo_vacio.txt"
archivo_vacio.touch(exist_ok=True)  # touch crea archivo vacío

# ---------------------------------------------------------
# 6️⃣ Leer y escribir archivos con Path
# ---------------------------------------------------------
# Leer contenido
# Path permite abrir archivos usando open(), igual que con strings
ruta_lectura = Path("ejemplo.txt")
if ruta_lectura.exists() and ruta_lectura.is_file():
    with ruta_lectura.open("r", encoding="utf-8") as f:
        contenido = f.read()
        print("Contenido leído:\n", contenido)

# Escribir contenido
ruta_escritura = Path("nueva_carpeta") / "salida.txt"
with ruta_escritura.open("w", encoding="utf-8") as f:
    f.write("Hola desde pathlib\n")
    f.write("Segunda línea\n")

# ---------------------------------------------------------
# 7️⃣ Iterar sobre archivos en una carpeta
# ---------------------------------------------------------
# Listar todos los archivos en una carpeta
for item in Path("nueva_carpeta").iterdir():
    if item.is_file():
        print("Archivo encontrado:", item.name)
    elif item.is_dir():
        print("Directorio encontrado:", item.name)

# Filtrar por extensión
txt_files = [f for f in Path("nueva_carpeta").iterdir() if f.suffix == ".txt"]
print("Archivos .txt:", txt_files)

# ---------------------------------------------------------
# 8️⃣ Ventajas de pathlib sobre os.path
# ---------------------------------------------------------
# ✅ Operador '/' para unir rutas de manera portable
# ✅ Métodos claros: .exists(), .is_file(), .is_dir(), .iterdir()
# ✅ Funciona con Path objects directamente, sin convertir a strings
# ✅ Facilita lectura/escritura de archivos con .open()
# ✅ Más legible y moderno que os.path

# ---------------------------------------------------------
# ✅ Conclusión
# ---------------------------------------------------------
# Pathlib es la forma profesional y moderna de manejar archivos y rutas en Python:
# - Objetos Path en lugar de cadenas
# - Métodos intuitivos para existencia, tipo y contenido
# - Portabilidad automática entre Windows, Linux y Mac
# - Integración perfecta con context managers
