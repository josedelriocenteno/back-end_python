"""
zipfile_usage.py
=================

GESTIÓN DE ARCHIVOS ZIP EN PYTHON
---------------------------------

Objetivo:
---------
Aprender a comprimir y descomprimir múltiples archivos usando el módulo estándar `zipfile`.
Esto es útil para:
- Agrupar datasets, logs o resultados de experimentos.
- Transferir múltiples archivos de forma compacta.
- Mantener pipelines reproducibles y ordenados.

Conceptos clave:
----------------
1. Un archivo ZIP puede contener múltiples archivos y carpetas.
2. Python ofrece el módulo `zipfile` para:
   - Crear archivos ZIP
   - Añadir archivos
   - Extraer archivos
   - Leer contenidos sin descomprimir
3. Útil en ML, Data y backend para empaquetar datos y logs.
"""

import zipfile
from pathlib import Path

# ============================================================
# 1️⃣ DEFINIR RUTAS
# ============================================================

CARPETA_DATOS = Path("data/")
ARCHIVO_ZIP = CARPETA_DATOS / "dataset_comprimido.zip"
ARCHIVO1 = CARPETA_DATOS / "dataset1.csv"
ARCHIVO2 = CARPETA_DATOS / "dataset2.csv"

# ============================================================
# 2️⃣ CREAR ZIP Y AÑADIR ARCHIVOS
# ============================================================

def crear_zip(archivos: list[Path], destino: Path) -> None:
    """
    Crea un archivo ZIP y añade los archivos listados.
    
    Args:
        archivos (list[Path]): Archivos a comprimir.
        destino (Path): Ruta del archivo ZIP.
    """
    # 'w' → write, sobrescribe si existe
    with zipfile.ZipFile(destino, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for archivo in archivos:
            if not archivo.exists():
                print(f"⚠️  Advertencia: {archivo} no existe, se omitirá.")
                continue
            # arcname es el nombre interno dentro del ZIP
            zipf.write(archivo, arcname=archivo.name)
            print(f"✅ Añadido al ZIP: {archivo.name}")

    print(f"Archivo ZIP creado: {destino}")


# ============================================================
# 3️⃣ LEER CONTENIDO DEL ZIP SIN EXTRAER
# ============================================================

def listar_zip(ruta_zip: Path) -> list[str]:
    """
    Lista los archivos contenidos en un ZIP sin extraerlos.
    
    Args:
        ruta_zip (Path): Ruta del ZIP.
    
    Returns:
        list[str]: Nombres de los archivos dentro del ZIP.
    """
    if not ruta_zip.exists():
        raise FileNotFoundError(f"No existe el ZIP: {ruta_zip}")

    with zipfile.ZipFile(ruta_zip, mode="r") as zipf:
        nombres = zipf.namelist()  # lista de archivos dentro del ZIP
    return nombres


# ============================================================
# 4️⃣ EXTRAER ARCHIVOS DEL ZIP
# ============================================================

def extraer_zip(ruta_zip: Path, destino: Path) -> None:
    """
    Extrae todos los archivos de un ZIP a la carpeta destino.
    
    Args:
        ruta_zip (Path): Archivo ZIP a extraer.
        destino (Path): Carpeta donde se extraen los archivos.
    """
    if not ruta_zip.exists():
        raise FileNotFoundError(f"No existe el ZIP: {ruta_zip}")

    with zipfile.ZipFile(ruta_zip, mode="r") as zipf:
        zipf.extractall(path=destino)
    print(f"Archivos extraídos en: {destino}")


# ============================================================
# 5️⃣ EJEMPLO COMPLETO DE USO
# ============================================================

def ejemplo_completo():
    """
    Flujo completo:
    1. Crear ZIP con múltiples archivos
    2. Listar su contenido
    3. Extraer los archivos a otra carpeta
    """
    archivos_a_comprimir = [ARCHIVO1, ARCHIVO2]

    # 1️⃣ Crear ZIP
    crear_zip(archivos_a_comprimir, ARCHIVO_ZIP)

    # 2️⃣ Listar archivos dentro del ZIP
    print("Contenido del ZIP:")
    for nombre in listar_zip(ARCHIVO_ZIP):
        print("-", nombre)

    # 3️⃣ Extraer archivos a carpeta temporal
    carpeta_destino = CARPETA_DATOS / "extraidos"
    carpeta_destino.mkdir(exist_ok=True)
    extraer_zip(ARCHIVO_ZIP, carpeta_destino)


# ============================================================
# 6️⃣ EJECUTAR
# ============================================================

if __name__ == "__main__":
    ejemplo_completo()
