"""
gzip_basico.py
================

LECTURA Y ESCRITURA DE ARCHIVOS COMPRIMIDOS CON GZIP EN PYTHON
--------------------------------------------------------------

Objetivo:
---------
Aprender a manejar archivos comprimidos usando el módulo estándar `gzip` de Python.
Este enfoque es esencial para:
- Guardar espacio en disco.
- Procesar grandes volúmenes de datos sin llenar la memoria.
- Mantener compatibilidad con sistemas que consumen archivos comprimidos.

Conceptos clave:
----------------
1. GZIP es un formato de compresión basado en DEFLATE.
2. Se puede leer y escribir archivos como si fueran normales, pero ocupan menos espacio.
3. Útil para logs, datasets CSV/JSON grandes, pipelines de ML, backups.
"""

import gzip
from pathlib import Path

# ============================================================
# 1️⃣ RUTA DEL ARCHIVO
# ============================================================

# Siempre usar pathlib para compatibilidad cross-platform
ARCHIVO_ORIGINAL = Path("data/dataset.csv")
ARCHIVO_COMPRESO = Path("data/dataset.csv.gz")


# ============================================================
# 2️⃣ ESCRIBIR ARCHIVO COMPRIMIDO
# ============================================================

def escribir_gzip(texto: str, ruta: Path) -> None:
    """
    Escribe un string en un archivo gzip.
    
    Args:
        texto (str): Contenido a guardar.
        ruta (Path): Ruta del archivo comprimido.
    """
    # 'wt' → write + texto
    # encoding='utf-8' para compatibilidad de caracteres
    with gzip.open(ruta, mode="wt", encoding="utf-8") as f:
        f.write(texto)
    print(f"Archivo comprimido creado: {ruta}")


# ============================================================
# 3️⃣ LEER ARCHIVO COMPRIMIDO
# ============================================================

def leer_gzip(ruta: Path) -> str:
    """
    Lee un archivo gzip y devuelve su contenido como string.
    
    Args:
        ruta (Path): Ruta del archivo comprimido.
    
    Returns:
        str: Contenido descomprimido.
    """
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    
    # 'rt' → read + texto
    with gzip.open(ruta, mode="rt", encoding="utf-8") as f:
        contenido = f.read()
    return contenido


# ============================================================
# 4️⃣ EJEMPLO DE USO
# ============================================================

def ejemplo_completo():
    """
    Muestra el flujo completo:
    1. Crear archivo original
    2. Comprimirlo
    3. Leerlo descomprimido
    """

    # 1️⃣ Contenido de ejemplo
    contenido_ejemplo = "id,nombre,edad\n1,Alice,30\n2,Bob,25\n3,Charlie,35"

    # 2️⃣ Guardar archivo comprimido
    escribir_gzip(contenido_ejemplo, ARCHIVO_COMPRESO)

    # 3️⃣ Leer contenido comprimido
    contenido_leido = leer_gzip(ARCHIVO_COMPRESO)

    print("Contenido leído desde gzip:")
    print(contenido_leido)


# ============================================================
# 5️⃣ EJECUTAR
# ============================================================

if __name__ == "__main__":
    ejemplo_completo()
