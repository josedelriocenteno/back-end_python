"""
limpieza_archivos_temporales.py
===============================

Manejo seguro y eficiente de archivos temporales en Python.

Objetivo:
---------
Evitar fugas de archivos temporales, liberar recursos y mantener higiene
en el sistema de archivos, mientras trabajamos con datos intermedios.
"""

import tempfile
import os
from pathlib import Path

# -----------------------------------------------------------
# 1️⃣ Por qué son importantes los archivos temporales
# -----------------------------------------------------------
"""
En muchos programas necesitamos guardar datos intermedios o caches,
por ejemplo:

- Resultados parciales de cálculos.
- Descargas temporales de la web.
- Archivos de logs de prueba.
- Procesamiento de datasets grandes.

Si no se eliminan correctamente:

- Ocupan espacio innecesario.
- Pueden contener datos sensibles.
- Pueden causar errores si se reutilizan nombres de archivos.
"""

# -----------------------------------------------------------
# 2️⃣ Crear archivos temporales
# -----------------------------------------------------------
"""
Python proporciona el módulo `tempfile` para manejar archivos y directorios temporales
de manera segura y portable.
"""

# 2.a. Archivo temporal básico
temp_file = tempfile.NamedTemporaryFile(delete=False)  # delete=False para controlar borrado manual
print(f"Archivo temporal creado: {temp_file.name}")

# Escribir contenido
temp_file.write(b"Datos temporales")
temp_file.close()  # Siempre cerrar para asegurar escritura

# Leer contenido
with open(temp_file.name, "rb") as f:
    print(f.read())

# 2.b. Archivo temporal con context manager (más seguro)
with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
    tmp.write("Datos temporales seguros")
    tmp.seek(0)
    contenido = tmp.read()
    print(f"Contenido dentro del context manager: {contenido}")
# Al salir del bloque, tmp se borra automáticamente

# -----------------------------------------------------------
# 3️⃣ Directorios temporales
# -----------------------------------------------------------
"""
A veces necesitamos crear varios archivos temporales juntos. Usamos TemporaryDirectory.
"""

with tempfile.TemporaryDirectory() as tmp_dir:
    print(f"Directorio temporal: {tmp_dir}")
    
    archivo1 = Path(tmp_dir) / "archivo1.txt"
    archivo1.write_text("Contenido archivo 1")
    
    archivo2 = Path(tmp_dir) / "archivo2.txt"
    archivo2.write_text("Contenido archivo 2")
    
    print("Archivos dentro del temporal:", list(Path(tmp_dir).iterdir()))

# Al salir del bloque, todo el directorio temporal se elimina automáticamente

# -----------------------------------------------------------
# 4️⃣ Buenas prácticas de limpieza
# -----------------------------------------------------------
"""
1. Siempre usar context managers cuando sea posible: `with`.
2. No confiar en borrar archivos manualmente: errores o excepciones pueden interrumpir el flujo.
3. Si se crean archivos temporales manualmente, borrarlos en un bloque `finally`:

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        temp_file.write(b"Algo importante")
    finally:
        os.remove(temp_file.name)

4. No usar nombres fijos para archivos temporales: siempre usar `NamedTemporaryFile` o `uuid`.
5. Controlar permisos si los archivos temporales contienen datos sensibles.
6. Evitar logs de archivos temporales que contengan información crítica.
"""

# -----------------------------------------------------------
# 5️⃣ Ejemplo completo: procesamiento de dataset temporal
# -----------------------------------------------------------

def procesar_dataset_temporal(data: str):
    """
    Simula procesamiento de datos guardando temporalmente en un archivo.
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
        # Guardar datos
        tmp.write(data)
        tmp.seek(0)
        
        # Procesar datos
        lineas = tmp.readlines()
        print("Número de líneas:", len(lineas))
        for i, linea in enumerate(lineas, start=1):
            print(f"Línea {i}: {linea.strip()}")
    # tmp se elimina automáticamente al salir del bloque

# Uso
procesar_dataset_temporal("linea1\nlinea2\nlinea3")

# -----------------------------------------------------------
# 6️⃣ Resumen
# -----------------------------------------------------------
"""
- `tempfile.NamedTemporaryFile` y `TemporaryDirectory` permiten crear archivos y directorios temporales de manera segura.
- Siempre usar context managers para asegurar limpieza automática.
- Evitar nombres fijos y controlar permisos.
- Nunca dejar archivos temporales con datos sensibles sin borrar.
- Permite mantener higiene y estabilidad en proyectos de cualquier tamaño.
"""
