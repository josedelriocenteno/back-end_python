"""
validacion_datasets.py
=======================

Objetivo:
- Validar datasets antes de usar en pipelines de ML o análisis
- Detectar errores de consistencia, duplicados, valores fuera de rango
- Facilitar la trazabilidad y reproducibilidad de los datos
"""

import pandas as pd
import logging

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO DE DATASET
# -------------------------------------------------------------------

datos = {
    "id": [1, 2, 3, 4, 5],
    "nombre": ["Alice", "Bob", "Charlie", None, "Eve"],
    "edad": [25, 30, -5, 40, 28],  # -5 → valor inválido
    "email": ["alice@mail.com", "bob@mail.com", "charlie@mail.com", "dave@mail.com", ""]
}

df = pd.DataFrame(datos)
print("Dataset inicial:\n", df)

# -------------------------------------------------------------------
# 2️⃣ FUNCIONES DE VALIDACIÓN
# -------------------------------------------------------------------

def validar_no_nulos(df: pd.DataFrame, columnas: list[str]):
    """
    Verifica que no existan valores nulos en columnas críticas
    """
    errores = {}
    for col in columnas:
        nulos = df[col].isnull().sum()
        if nulos > 0:
            errores[col] = nulos
            logging.warning(f"{nulos} valores nulos en columna '{col}'")
    return errores

def validar_edad(df: pd.DataFrame, min_val=0, max_val=120):
    """
    Valida que la edad esté en rango permitido
    """
    invalidas = df[(df["edad"] < min_val) | (df["edad"] > max_val)]
    if not invalidas.empty:
        logging.warning(f"Edades fuera de rango detectadas:\n{invalidas[['id','edad']]}")
    return invalidas

def validar_duplicados(df: pd.DataFrame, columnas: list[str]):
    """
    Detecta duplicados basados en columnas clave
    """
    dup = df[df.duplicated(subset=columnas, keep=False)]
    if not dup.empty:
        logging.warning(f"Duplicados detectados:\n{dup}")
    return dup

def validar_emails(df: pd.DataFrame, columna="email"):
    """
    Verifica que los emails no estén vacíos y tengan formato básico
    """
    import re
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    invalidos = df[~df[columna].str.match(patron, na=False)]
    if not invalidos.empty:
        logging.warning(f"Emails inválidos:\n{invalidos[[columna,'id']]}")
    return invalidos

# -------------------------------------------------------------------
# 3️⃣ VALIDACIÓN CENTRALIZADA
# -------------------------------------------------------------------

def validar_dataset(df: pd.DataFrame):
    """
    Ejecuta todas las validaciones principales
    """
    errores = {}
    errores["nulos"] = validar_no_nulos(df, ["nombre"])
    errores["edad"] = validar_edad(df)
    errores["duplicados"] = validar_duplicados(df, ["id"])
    errores["emails"] = validar_emails(df)
    
    if any(len(v) > 0 if isinstance(v, dict) else not v.empty for v in errores.values()):
        logging.warning("Dataset tiene problemas. Revisar logs.")
    else:
        logging.info("Dataset validado correctamente, listo para pipeline.")
    
    return errores

# -------------------------------------------------------------------
# 4️⃣ EJECUCIÓN DE VALIDACIÓN
# -------------------------------------------------------------------

errores_detectados = validar_dataset(df)
print("\nErrores detectados:\n", errores_detectados)

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Centralizar validaciones para todos los datasets
# 2️⃣ No detener el pipeline por errores recuperables, registrar y limpiar
# 3️⃣ Mantener logs estructurados con contexto (id, fila, columna)
# 4️⃣ Validar tipos, nulos, duplicados, rangos, consistencia de datos
# 5️⃣ Separar lógica de validación de transformación de datos
# 6️⃣ Automatizar checks antes de entrenamiento o ETL
# 7️⃣ Permitir reproducibilidad y trazabilidad de errores
