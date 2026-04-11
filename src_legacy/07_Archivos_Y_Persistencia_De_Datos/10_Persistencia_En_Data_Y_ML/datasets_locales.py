"""
datasets_locales.py
===================

OBJETIVO
--------
Proporcionar patrones y buenas prácticas para manejar datasets locales de
forma profesional: rutas consistentes, validación, carga y almacenamiento
eficiente y reproducible para proyectos de análisis de datos o ML.

TODO se explica paso a paso, sin asumir conocimientos previos.
"""

from pathlib import Path
import pandas as pd
import json
from typing import Optional

# ============================================================
# 1️⃣ Definir carpeta base de datasets
# ============================================================
# Siempre trabajar con rutas absolutas relativas al proyecto.
# Evita errores de path relativos o confusos.
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "datasets"
DATA_DIR.mkdir(exist_ok=True)  # Crear si no existe

# ============================================================
# 2️⃣ Definir funciones de carga de datasets
# ============================================================

def cargar_csv(nombre_archivo: str, separator: str = ",") -> Optional[pd.DataFrame]:
    """
    Carga un CSV desde la carpeta de datasets.

    Args:
        nombre_archivo (str): nombre del archivo CSV
        separator (str): separador del CSV, por defecto ','
    
    Returns:
        pd.DataFrame o None si hay error
    """
    path = DATA_DIR / nombre_archivo
    if not path.exists():
        print(f"Error: archivo CSV no encontrado: {path}")
        return None

    try:
        df = pd.read_csv(path, sep=separator)
        print(f"Dataset cargado correctamente: {path}")
        return df
    except pd.errors.EmptyDataError:
        print(f"Error: archivo CSV vacío: {path}")
        return None
    except pd.errors.ParserError as e:
        print(f"Error: fallo al parsear CSV: {path} | Detalle: {e}")
        return None

def cargar_json(nombre_archivo: str) -> Optional[dict]:
    """
    Carga un JSON desde la carpeta de datasets.

    Args:
        nombre_archivo (str): nombre del archivo JSON
    
    Returns:
        dict o None si hay error
    """
    path = DATA_DIR / nombre_archivo
    if not path.exists():
        print(f"Error: archivo JSON no encontrado: {path}")
        return None
    
    try:
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"JSON cargado correctamente: {path}")
        return data
    except json.JSONDecodeError as e:
        print(f"Error: JSON corrupto: {path} | Detalle: {e}")
        return None

# ============================================================
# 3️⃣ Guardar datasets de manera profesional
# ============================================================

def guardar_csv(df: pd.DataFrame, nombre_archivo: str, separator: str = ",", versionar: bool = True):
    """
    Guarda un DataFrame como CSV, con opción a versionado.
    
    Args:
        df (pd.DataFrame): dataset a guardar
        nombre_archivo (str): nombre de archivo final
        separator (str): separador CSV
        versionar (bool): si True crea backup de la versión anterior
    """
    path = DATA_DIR / nombre_archivo
    
    if versionar and path.exists():
        backup_path = DATA_DIR / f"{nombre_archivo}.bak"
        path.replace(backup_path)
        print(f"Backup creado: {backup_path}")
    
    df.to_csv(path, sep=separator, index=False)
    print(f"Dataset guardado: {path}")

def guardar_json(data: dict, nombre_archivo: str, versionar: bool = True):
    """
    Guarda un diccionario como JSON, con opción a versionado.
    
    Args:
        data (dict): datos a guardar
        nombre_archivo (str): nombre de archivo final
        versionar (bool): si True crea backup de la versión anterior
    """
    path = DATA_DIR / nombre_archivo
    if versionar and path.exists():
        backup_path = DATA_DIR / f"{nombre_archivo}.bak"
        path.replace(backup_path)
        print(f"Backup creado: {backup_path}")
    
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"JSON guardado: {path}")

# ============================================================
# 4️⃣ Validación mínima de datasets
# ============================================================
def validar_dataset_csv(df: pd.DataFrame, columnas_requeridas: list[str]) -> bool:
    """
    Verifica que el DataFrame contenga todas las columnas requeridas.
    
    Args:
        df (pd.DataFrame)
        columnas_requeridas (list[str])
    
    Returns:
        bool
    """
    if df is None:
        print("Error: DataFrame es None")
        return False
    
    faltantes = [col for col in columnas_requeridas if col not in df.columns]
    if faltantes:
        print(f"Error: columnas faltantes en dataset: {faltantes}")
        return False
    
    return True

# ============================================================
# 5️⃣ Ejemplo de uso completo
# ============================================================
if __name__ == "__main__":
    # Crear un DataFrame de ejemplo
    df_ejemplo = pd.DataFrame({
        "id": [1, 2, 3],
        "nombre": ["Alice", "Bob", "Charlie"],
        "edad": [25, 30, 35]
    })
    
    # Guardar CSV con versionado
    guardar_csv(df_ejemplo, "usuarios.csv")
    
    # Cargar CSV
    df_cargado = cargar_csv("usuarios.csv")
    
    # Validar columnas
    if validar_dataset_csv(df_cargado, ["id", "nombre", "edad"]):
        print("Dataset validado correctamente")
    
    # Guardar JSON
    data_dict = {"usuarios": df_ejemplo.to_dict(orient="records")}
    guardar_json(data_dict, "usuarios.json")
    
    # Cargar JSON
    data_cargada = cargar_json("usuarios.json")
