"""
parquet_lectura.py
==================

LECTURA DE ARCHIVOS PARQUET CON PYARROW Y PANDAS
-----------------------------------------------

Este archivo explica DESDE CERO cómo se leen archivos Parquet en Python,
por qué existen varias formas de hacerlo y cuándo usar cada una.

Nada aquí se da por supuesto.
"""

# ============================================================
# 1. PRIMERA PREGUNTA CLAVE
# ============================================================
# ¿Qué significa "leer un archivo Parquet"?
#
# Significa:
# - Acceder a datos que están guardados en disco
# - Convertirlos a una estructura en memoria (RAM)
# - Poder trabajar con ellos en Python
#
# Parquet NO se puede leer "a mano" como un CSV.
# Necesitamos LIBRERÍAS especializadas.
# ============================================================


# ============================================================
# 2. LAS DOS LIBRERÍAS PRINCIPALES
# ============================================================
# En Python hay dos caminos habituales:
#
# 1) pyarrow  → bajo nivel, muy eficiente, más control
# 2) pandas   → alto nivel, más cómodo, más común
#
# IMPORTANTE:
# Pandas INTERNAMENTE usa pyarrow para Parquet.
# ============================================================

import pandas as pd  # Librería principal para data analysis
import pyarrow.parquet as pq  # Lectura directa de Parquet
import pyarrow as pa  # Estructuras internas de Arrow


# ============================================================
# 3. RUTA DEL ARCHIVO
# ============================================================
# Nunca "hardcodees" rutas raras.
# Aquí asumimos que el archivo existe.
# ============================================================

PARQUET_PATH = "data/ejemplo.parquet"


# ============================================================
# 4. OPCIÓN 1: LEER PARQUET CON PANDAS (LA MÁS COMÚN)
# ============================================================
# Esta es la forma que verás en el 80% de proyectos Data.
# ============================================================

def leer_parquet_con_pandas(ruta: str) -> pd.DataFrame:
    """
    Lee un archivo Parquet usando pandas.

    Parámetros
    ----------
    ruta : str
        Ruta al archivo .parquet

    Retorna
    -------
    pd.DataFrame
        DataFrame cargado en memoria
    """

    # pd.read_parquet:
    # - Detecta automáticamente el engine (pyarrow)
    # - Respeta tipos (int, float, datetime, etc.)
    # - Es MUCHO más rápido que CSV

    df = pd.read_parquet(ruta)

    return df


# ============================================================
# 5. QUÉ PASA INTERNAMENTE AQUÍ (IMPORTANTE)
# ============================================================
# Cuando haces:
#
#   pd.read_parquet(...)
#
# Pandas:
# 1) Usa pyarrow
# 2) Lee columnas de forma eficiente
# 3) Convierte Arrow → DataFrame
#
# Tú no lo ves, pero pasa.
# ============================================================


# ============================================================
# 6. OPCIÓN 2: LEER PARQUET CON PYARROW DIRECTAMENTE
# ============================================================
# Esto se usa cuando:
# - Dataset muy grande
# - Necesitas control fino
# - No quieres cargar todo en RAM
# ============================================================

def leer_parquet_con_pyarrow(ruta: str) -> pa.Table:
    """
    Lee un archivo Parquet usando pyarrow directamente.

    Retorna una pyarrow.Table (NO un DataFrame).
    """

    # pq.read_table:
    # - Devuelve una tabla columnar en memoria
    # - Muy eficiente
    # - Ideal para pipelines grandes

    table = pq.read_table(ruta)

    return table


# ============================================================
# 7. DIFERENCIA CLAVE: DataFrame vs Arrow Table
# ============================================================
#
# pd.DataFrame:
# - Pensado para análisis interactivo
# - Muy cómodo
#
# pa.Table:
# - Pensado para rendimiento
# - Columnar puro
# - Mejor para ML pipelines grandes
# ============================================================


# ============================================================
# 8. CONVERSIÓN: PYARROW → PANDAS
# ============================================================
# A veces quieres:
# - Leer eficientemente
# - Luego trabajar con pandas
# ============================================================

def arrow_a_pandas(table: pa.Table) -> pd.DataFrame:
    """
    Convierte una tabla Arrow a DataFrame pandas.
    """

    # to_pandas:
    # - Hace la conversión explícita
    # - Aquí es donde se usa RAM
    df = table.to_pandas()

    return df


# ============================================================
# 9. LECTURA SELECTIVA DE COLUMNAS (CLAVE DE PARQUET)
# ============================================================
# Esto es una de las GRANDES ventajas de Parquet.
# ============================================================

def leer_solo_columnas(ruta: str, columnas: list[str]) -> pd.DataFrame:
    """
    Lee SOLO ciertas columnas de un archivo Parquet.

    Esto es IMPOSIBLE de hacer eficientemente con CSV.
    """

    df = pd.read_parquet(
        ruta,
        columns=columnas  # <- magia del columnar storage
    )

    return df


# ============================================================
# 10. EJEMPLO REAL DE USO
# ============================================================

def ejemplo_real():
    """
    Simula un flujo real de trabajo.
    """

    # Leer dataset completo
    df_completo = leer_parquet_con_pandas(PARQUET_PATH)

    print("Dataset completo:")
    print(df_completo.head())

    # Leer solo columnas necesarias
    df_reducido = leer_solo_columnas(
        PARQUET_PATH,
        columnas=["edad", "ingresos"]
    )

    print("\nSolo columnas necesarias:")
    print(df_reducido.head())


# ============================================================
# 11. ERRORES COMUNES QUE DEBES EVITAR
# ============================================================
#
# ❌ Cargar Parquet gigante completo "porque sí"
# ❌ Convertir a CSV después
# ❌ Usar CSV para ML serio
# ❌ Ignorar tipos
#
# ============================================================


# ============================================================
# 12. IDEA CLAVE QUE DEBES RECORDAR
# ============================================================
#
# CSV:
# - Fácil
# - Lento
# - Frágil
#
# Parquet:
# - Profesional
# - Rápido
# - Reproducible
#
# ============================================================


if __name__ == "__main__":
    # Esto solo se ejecuta si lanzas este archivo directamente
    ejemplo_real()
