"""
errores_comunes_backend.py
==========================

OBJETIVO
--------
Identificar y prevenir errores frecuentes al manejar persistencia de archivos
en aplicaciones backend. Esto incluye manejo de rutas, concurrencia, permisos,
lectura/escritura de archivos y buenas prácticas generales.

CADA SECCIÓN EXPLICA EL ERROR, POR QUÉ OCURRE Y CÓMO EVITARLO.
"""

from pathlib import Path
import json
import os

# ============================================================
# 1️⃣ Error: Paths relativos y mal construidos
# ============================================================
# Problema: Usar rutas relativas sin consistencia puede romper la app en producción
# Ejemplo típico:
# archivo = "config/settings.json"
# Esto funciona localmente, pero falla si se ejecuta desde otra carpeta.

# Solución profesional: usar pathlib y rutas absolutas relativas al script o proyecto
BASE_DIR = Path(__file__).parent  # carpeta del script actual
CONFIG_PATH = BASE_DIR / "config" / "settings.json"

if not CONFIG_PATH.exists():
    print("Advertencia: archivo de configuración no existe:", CONFIG_PATH)

# ============================================================
# 2️⃣ Error: No manejar concurrencia al escribir archivos
# ============================================================
# Problema: Si varios procesos o threads escriben el mismo archivo simultáneamente,
# se puede corromper el contenido.

# Solución: usar locking o almacenamiento transaccional
# Ejemplo sencillo de escritura segura con modo 'x' (fallará si ya existe)
def guardar_archivo_seguro(path: Path, contenido: str):
    try:
        with path.open('x', encoding='utf-8') as f:  # 'x' = solo si no existe
            f.write(contenido)
        print("Archivo guardado correctamente:", path)
    except FileExistsError:
        print("Error: archivo ya existe, no se sobrescribe para evitar corrupción")

# ============================================================
# 3️⃣ Error: No manejar errores de lectura/escritura
# ============================================================
# Problema: Abrir archivos sin try/except genera fallos que crashan el backend
# Ejemplo:
# data = open("archivo_inexistente.txt").read()  # RuntimeError si no existe

# Solución: capturar excepciones específicas
def leer_json_seguro(path: Path):
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: archivo no encontrado:", path)
    except json.JSONDecodeError as e:
        print("Error: JSON corrupto en archivo:", path, "| Detalle:", e)
    return None

# ============================================================
# 4️⃣ Error: Sobrescribir datos críticos sin backup
# ============================================================
# Problema: Al actualizar archivos importantes, se pierden datos anteriores.

# Solución: versionado o backup automático
def guardar_con_backup(path: Path, contenido: str):
    if path.exists():
        backup_path = path.with_suffix(".bak")
        path.replace(backup_path)
        print("Backup creado:", backup_path)
    with path.open('w', encoding='utf-8') as f:
        f.write(contenido)
    print("Archivo actualizado:", path)

# ============================================================
# 5️⃣ Error: Permisos incorrectos
# ============================================================
# Problema: Archivos que no pueden leerse/escribirse por el backend
# Solución: definir permisos claros y usar pathlib para verificarlos
def verificar_permisos(path: Path):
    if not os.access(path, os.R_OK):
        print("Error: archivo no tiene permiso de lectura:", path)
    if not os.access(path, os.W_OK):
        print("Error: archivo no tiene permiso de escritura:", path)

# ============================================================
# 6️⃣ Error: No limpiar archivos temporales
# ============================================================
# Problema: Acumulación de archivos tmp genera consumo de disco y errores
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

def crear_archivo_temp(nombre: str, contenido: str):
    temp_file = TEMP_DIR / nombre
    with temp_file.open('w', encoding='utf-8') as f:
        f.write(contenido)
    print("Archivo temporal creado:", temp_file)
    return temp_file

def limpiar_archivos_temp():
    for archivo in TEMP_DIR.iterdir():
        archivo.unlink()
    print("Archivos temporales eliminados")

# ============================================================
# 7️⃣ Error: No validar input de archivos externos
# ============================================================
# Problema: Datos corruptos, mal formateados o inesperados pueden romper la app
# Solución: siempre validar contenido antes de procesar
def validar_json(path: Path) -> bool:
    data = leer_json_seguro(path)
    if data is None:
        return False
    # Ejemplo: esperar que sea un dict con clave 'name'
    if not isinstance(data, dict) or 'name' not in data:
        print("Error: estructura de JSON incorrecta en", path)
        return False
    return True

# ============================================================
# 8️⃣ Error: No usar paths seguros (path traversal)
# ============================================================
# Problema: usuarios maliciosos pueden acceder a archivos fuera de directorio permitido
# Solución: usar pathlib y validar que path está dentro del directorio esperado
def path_seguro(base: Path, target: Path) -> bool:
    try:
        return base.resolve() in target.resolve().parents or base.resolve() == target.resolve()
    except Exception:
        return False

# ============================================================
# Resumen de buenas prácticas
# ============================================================
"""
1. Usar pathlib para paths consistentes y seguros.
2. Manejar errores específicos (FileNotFoundError, JSONDecodeError, PermissionError).
3. Hacer backups o versionado antes de sobrescribir datos importantes.
4. Validar datos de entrada antes de procesarlos.
5. Limpiar archivos temporales para no saturar el disco.
6. Evitar accesos a paths fuera de directorio permitido.
7. Gestionar concurrencia al escribir archivos compartidos.
8. Separar almacenamiento local de cloud según necesidad y tamaño de datos.
"""
