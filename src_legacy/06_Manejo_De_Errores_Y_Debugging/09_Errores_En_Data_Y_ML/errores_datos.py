"""
errores_datos.py
=================

Objetivo:
- Detectar y manejar datos corruptos o inconsistentes
- Evitar que errores en los datos rompan pipelines de ETL o ML
- Facilitar trazabilidad y limpieza profesional
"""

import pandas as pd
import logging

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO DE DATOS CORRUPTOS
# -------------------------------------------------------------------

datos = {
    "id": [1, 2, 3, 4],
    "nombre": ["Alice", "Bob", None, "David"],  # None → dato faltante
    "edad": [25, -1, 30, 27],  # -1 → valor inválido
    "email": ["alice@mail.com", "bob@mail.com", "charlie@mail.com", ""]  # "" vacío
}

df = pd.DataFrame(datos)

print("Datos iniciales:\n", df)

# -------------------------------------------------------------------
# 2️⃣ DETECCIÓN DE DATOS PROBLEMÁTICOS
# -------------------------------------------------------------------

# a) Valores nulos
nulos = df.isnull().sum()
print("\nValores nulos por columna:\n", nulos)

# b) Valores vacíos o inválidos
vacios = (df == "").sum()
print("\nValores vacíos por columna:\n", vacios)

# c) Reglas de negocio (edad >= 0)
errores_edad = df[df["edad"] < 0]
print("\nErrores en edad:\n", errores_edad)

# -------------------------------------------------------------------
# 3️⃣ MANEJO PROFESIONAL DE DATOS CORRUPTOS
# -------------------------------------------------------------------

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función profesional de limpieza de datos:
    - Elimina o corrige filas con errores críticos
    - Registra errores para trazabilidad
    """
    df_limpio = df.copy()

    # Manejo de nulos
    if df_limpio["nombre"].isnull().any():
        n = df_limpio["nombre"].isnull().sum()
        logging.warning(f"{n} nombres nulos detectados. Se reemplazarán por 'Desconocido'.")
        df_limpio["nombre"].fillna("Desconocido", inplace=True)

    # Manejo de valores vacíos
    if (df_limpio["email"] == "").any():
        n = (df_limpio["email"] == "").sum()
        logging.warning(f"{n} emails vacíos detectados. Se reemplazarán por 'no_email@unknown.com'.")
        df_limpio.loc[df_limpio["email"] == "", "email"] = "no_email@unknown.com"

    # Reglas de negocio: edad positiva
    df_limpio = df_limpio[df_limpio["edad"] >= 0]
    if len(df_limpio) < len(df):
        logging.warning("Filas con edad inválida eliminadas.")

    return df_limpio

df_limpio = limpiar_datos(df)
print("\nDatos limpios:\n", df_limpio)

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Detectar datos faltantes, vacíos o fuera de rango
# 2️⃣ Aplicar reglas de negocio para validación
# 3️⃣ Registrar warnings y errores para trazabilidad
# 4️⃣ Evitar detener todo el pipeline por errores de datos recuperables
# 5️⃣ Centralizar funciones de validación y limpieza
# 6️⃣ Mantener logs claros y estructurados para debugging posterior
# 7️⃣ Separar la capa de validación de la lógica de ML o procesamiento
