"""
paths_seguridad.py
==================
Evitar vulnerabilidades relacionadas con rutas de archivos (Path Traversal).

Objetivo:
---------
Aprender a manejar rutas de archivos en Python de forma segura para evitar
que un usuario malintencionado acceda a archivos que no debería.
"""

import os
from pathlib import Path

# -----------------------------------------------------------
# 1️⃣ Qué es Path Traversal
# -----------------------------------------------------------
"""
Path Traversal (o Directory Traversal) ocurre cuando un atacante puede
modificar la ruta de un archivo que un programa va a leer o escribir,
permitiéndole acceder a archivos arbitrarios del sistema.

Ejemplo inseguro:

    archivo = input("Nombre del archivo a leer: ")
    with open(f"/home/proyecto/{archivo}", "r") as f:
        contenido = f.read()
    
Si el usuario ingresa "../../etc/passwd", podría leer archivos sensibles
fuera del directorio permitido.
"""

# -----------------------------------------------------------
# 2️⃣ Validación básica de rutas
# -----------------------------------------------------------
# Supongamos que solo queremos acceder a archivos dentro de un directorio seguro:
BASE_DIR = Path("/home/proyecto/archivos_seguro")

def leer_archivo_seguro(nombre_archivo: str) -> str:
    """
    Lee un archivo dentro del directorio BASE_DIR, evitando path traversal.
    """
    # Convertir a Path absoluto
    ruta_objetivo = (BASE_DIR / nombre_archivo).resolve()

    # Verificar que ruta_objetivo esté dentro de BASE_DIR
    if not str(ruta_objetivo).startswith(str(BASE_DIR.resolve())):
        raise ValueError("Intento de acceso fuera del directorio permitido")

    # Leer archivo de forma segura
    with open(ruta_objetivo, "r", encoding="utf-8") as f:
        return f.read()

# -----------------------------------------------------------
# 3️⃣ Uso de pathlib para rutas seguras
# -----------------------------------------------------------
"""
pathlib.Path es preferible sobre concatenar strings porque:

- Permite convertir a rutas absolutas.
- Facilita validar subdirectorios.
- Funciona de forma portable entre Windows y Linux.
"""

def crear_archivo_seguro(nombre_archivo: str, contenido: str):
    ruta_objetivo = (BASE_DIR / nombre_archivo).resolve()
    if not str(ruta_objetivo).startswith(str(BASE_DIR.resolve())):
        raise ValueError("Intento de acceso fuera del directorio permitido")
    
    ruta_objetivo.parent.mkdir(parents=True, exist_ok=True)  # crear directorios si faltan
    with open(ruta_objetivo, "w", encoding="utf-8") as f:
        f.write(contenido)

# -----------------------------------------------------------
# 4️⃣ Buenas prácticas
# -----------------------------------------------------------
"""
1. No concatenar strings para rutas de archivos recibidos de usuarios.
2. Usar Path.resolve() para obtener rutas absolutas y comparar con la base segura.
3. Nunca confiar en la entrada del usuario.
4. Limitar la operación de archivos a un directorio específico.
5. Considerar permisos de archivos (solo lectura/escritura según necesidad).
"""

# -----------------------------------------------------------
# 5️⃣ Ejemplo completo
# -----------------------------------------------------------
if __name__ == "__main__":
    try:
        crear_archivo_seguro("datos.txt", "Contenido seguro")
        print(leer_archivo_seguro("datos.txt"))

        # Intento de path traversal (debería fallar)
        leer_archivo_seguro("../../etc/passwd")
    except Exception as e:
        print(f"Error de seguridad: {e}")
