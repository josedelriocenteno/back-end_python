# os_path.py
# =======================
# Manejo de rutas y sistema de archivos en Python usando os.path
# Explicación detallada de join, exists, isfile y buenas prácticas

import os  # Módulo estándar para interactuar con el sistema de archivos

# ---------------------------------------------------------
# 1️⃣ Construir rutas seguras con os.path.join()
# ---------------------------------------------------------
# Problema: concatenar rutas usando '+' o '/' no es seguro
# Diferencias entre sistemas operativos:
# - Windows: usa '\'
# - Linux/Mac: usa '/'

# Ejemplo incorrecto:
ruta = "carpeta" + "/" + "archivo.txt"
print("Ruta concatenada manual:", ruta)

# Problema: en Windows las barras invertidas pueden causar errores

# Solución profesional: os.path.join()
carpeta = "mi_carpeta"
archivo = "archivo.txt"
ruta_segura = os.path.join(carpeta, archivo)
print("Ruta segura:", ruta_segura)

# os.path.join() ajusta automáticamente las barras según el sistema operativo

# ---------------------------------------------------------
# 2️⃣ Verificar si un archivo o carpeta existe
# ---------------------------------------------------------
# os.path.exists(ruta) → True si existe (archivo o carpeta), False si no

if os.path.exists(ruta_segura):
    print(f"El archivo o carpeta '{ruta_segura}' existe")
else:
    print(f"'{ruta_segura}' no existe")

# Esto es útil para evitar errores al abrir archivos inexistentes

# ---------------------------------------------------------
# 3️⃣ Diferenciar archivos y carpetas
# ---------------------------------------------------------
# os.path.isfile(ruta) → True si es un archivo regular
# os.path.isdir(ruta) → True si es una carpeta/directorio

if os.path.isfile(ruta_segura):
    print(f"'{ruta_segura}' es un archivo")
elif os.path.isdir(ruta_segura):
    print(f"'{ruta_segura}' es un directorio")
else:
    print(f"'{ruta_segura}' no es ni archivo ni directorio")

# Esto permite validar antes de leer/escribir o listar directorios

# ---------------------------------------------------------
# 4️⃣ Obtener información adicional de rutas
# ---------------------------------------------------------
print("Nombre base (archivo con extensión):", os.path.basename(ruta_segura))
print("Directorio contenedor:", os.path.dirname(ruta_segura))
print("Ruta absoluta:", os.path.abspath(ruta_segura))
print("Separador de rutas del sistema:", os.path.sep)

# ---------------------------------------------------------
# 5️⃣ Combinar rutas dinámicamente
# ---------------------------------------------------------
# Supongamos que tenemos varias carpetas y queremos crear una ruta completa
base = "/home/usuario"
subcarpeta = "documentos"
nombre_archivo = "datos.csv"

ruta_completa = os.path.join(base, subcarpeta, nombre_archivo)
print("Ruta completa combinada:", ruta_completa)

# ---------------------------------------------------------
# 6️⃣ Buenas prácticas con os.path
# ---------------------------------------------------------
# ✅ Usar os.path.join en lugar de concatenar con '+' o '/'
# ✅ Verificar existencia con os.path.exists antes de abrir archivos
# ✅ Diferenciar archivos y carpetas con isfile/isdir
# ✅ Obtener ruta absoluta si es necesario, con abspath
# ✅ Evitar hardcodear rutas con separadores específicos de SO

# ---------------------------------------------------------
# 7️⃣ Ejemplo completo: abrir archivo seguro
# ---------------------------------------------------------
# Solo abrir si existe y es un archivo
if os.path.exists(ruta_segura) and os.path.isfile(ruta_segura):
    with open(ruta_segura, "r", encoding="utf-8") as f:
        contenido = f.read()
        print("Contenido del archivo:\n", contenido)
else:
    print(f"No se puede abrir '{ruta_segura}', archivo no válido")

# ---------------------------------------------------------
# ✅ Conclusión
# ---------------------------------------------------------
# Usar os.path permite:
# - Crear rutas portables y seguras
# - Verificar existencia de archivos y carpetas
# - Evitar errores por rutas mal construidas
# - Trabajar de manera consistente en Windows, Linux y Mac
