"""
parquet_escritura.py
===================

ESCRITURA DE ARCHIVOS PARQUET EN PYTHON
--------------------------------------

Este archivo explica, DESDE CERO, cómo escribir archivos Parquet de forma
profesional, eficiente y preparada para proyectos de Data y ML reales.

Aquí no solo "guardamos datos":
- Diseñamos schemas
- Elegimos compresión
- Pensamos en rendimiento
- Evitamos errores típicos

Nada se da por supuesto.
"""

# ============================================================
# 1. QUÉ SIGNIFICA "ESCRIBIR PARQUET"
# ============================================================
# Escribir Parquet significa:
#
# - Tomar datos que están en memoria (RAM)
# - Convertirlos a formato columnar binario
# - Guardarlos en disco de forma eficiente
#
# NO es lo mismo que guardar CSV.
# Aquí estamos tomando decisiones IMPORTANTES.
# ============================================================


# ============================================================
# 2. LIBRERÍAS NECESARIAS
# ============================================================
# Usaremos:
# - pandas → para DataFrames
# - pyarrow → para control fino y profesional
# ============================================================

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path


# ============================================================
# 3. RUTA DE SALIDA
# ============================================================
# Usamos pathlib porque:
# - Es portable
# - Es más segura
# - Es más clara
# ============================================================

OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PARQUET_PATH = OUTPUT_DIR / "dataset.parquet"


# ============================================================
# 4. CREAR UN DATASET DE EJEMPLO
# ============================================================
# Antes de escribir Parquet, necesitamos datos en memoria.
# ============================================================

def crear_dataframe_ejemplo() -> pd.DataFrame:
    """
    Crea un DataFrame de ejemplo simulando datos reales.
    """

    data = {
        "id": [1, 2, 3, 4],
        "edad": [25, 32, 40, 29],
        "pais": ["ES", "ES", "MX", "AR"],
        "ingresos": [30000.0, 45000.0, 38000.0, 41000.0],
    }

    df = pd.DataFrame(data)

    return df


# ============================================================
# 5. ESCRITURA SIMPLE CON PANDAS
# ============================================================
# Esta es la forma más común y más sencilla.
# ============================================================

def escribir_parquet_con_pandas(df: pd.DataFrame, ruta: Path) -> None:
    """
    Escribe un DataFrame a Parquet usando pandas.
    """

    # pd.DataFrame.to_parquet:
    # - Usa pyarrow internamente
    # - Mantiene tipos
    # - Aplica compresión por defecto (snappy)

    df.to_parquet(
        ruta,
        engine="pyarrow",
        index=False  # MUY IMPORTANTE: no guardes el índice si no lo necesitas
    )


# ============================================================
# 6. QUÉ ACABA DE PASAR REALMENTE
# ============================================================
# Pandas:
# - Convierte DataFrame → Arrow Table
# - Aplica compresión
# - Escribe columnas separadas
#
# Todo eso sin que tú lo veas.
# ============================================================


# ============================================================
# 7. ESCRITURA PROFESIONAL CON PYARROW
# ============================================================
# Aquí tenemos control total.
# ============================================================

def escribir_parquet_con_pyarrow(df: pd.DataFrame, ruta: Path) -> None:
    """
    Escribe Parquet usando pyarrow directamente.
    """

    # Convertimos DataFrame → Arrow Table explícitamente
    table = pa.Table.from_pandas(df)

    # Escribimos el archivo con opciones avanzadas
    pq.write_table(
        table,
        ruta,
        compression="snappy",  # rápida y equilibrada
        use_dictionary=True,   # ideal para columnas repetidas (pais)
        write_statistics=True  # permite optimizaciones en lectura
    )


# ============================================================
# 8. COMPRESIÓN: NO ES UN DETALLE
# ============================================================
#
# Opciones comunes:
#
# - snappy  → rápida, equilibrio (default)
# - gzip    → más compacta, más lenta
# - brotli  → muy compacta, CPU más cara
#
# Regla general:
# - ML / pipelines → snappy
# - Almacenamiento → gzip
#
# ============================================================


# ============================================================
# 9. SCHEMA EXPLÍCITO (NIVEL PRO)
# ============================================================
# Definir schema evita errores silenciosos.
# ============================================================

def escribir_con_schema_explicito(df: pd.DataFrame, ruta: Path) -> None:
    """
    Escribe Parquet definiendo el schema manualmente.
    """

    schema = pa.schema([
        ("id", pa.int64()),
        ("edad", pa.int64()),
        ("pais", pa.string()),
        ("ingresos", pa.float64()),
    ])

    table = pa.Table.from_pandas(df, schema=schema)

    pq.write_table(
        table,
        ruta,
        compression="snappy"
    )


# ============================================================
# 10. POR QUÉ EL SCHEMA ES CRÍTICO EN ML
# ============================================================
#
# Sin schema:
# - Tipos pueden cambiar
# - Errores invisibles
#
# Con schema:
# - Reproducibilidad
# - Pipelines estables
# - Menos bugs
#
# ============================================================


# ============================================================
# 11. PARTICIONADO (CONCEPTO CLAVE)
# ============================================================
# No escribimos aquí el código completo todavía,
# pero entiende la idea:
#
# data/
#   pais=ES/
#     part.parquet
#   pais=MX/
#     part.parquet
#
# Esto permite leer solo un país sin tocar los demás.
# ============================================================


# ============================================================
# 12. EJEMPLO COMPLETO
# ============================================================

def ejemplo_completo():
    df = crear_dataframe_ejemplo()

    print("DataFrame original:")
    print(df)

    escribir_parquet_con_pandas(df, PARQUET_PATH)
    print(f"\nParquet escrito con pandas en: {PARQUET_PATH}")

    escribir_parquet_con_pyarrow(df, PARQUET_PATH)
    print("Parquet escrito con pyarrow (control avanzado)")

    escribir_con_schema_explicito(df, PARQUET_PATH)
    print("Parquet escrito con schema explícito")


# ============================================================
# 13. ERRORES MUY COMUNES (EVÍTALOS)
# ============================================================
#
# ❌ Guardar índice sin querer
# ❌ No definir schema en ML
# ❌ Usar CSV para datasets grandes
# ❌ Reescribir Parquet con schema distinto
#
# ============================================================


# ============================================================
# 14. IDEA FINAL QUE DEBES TENER CLARA
# ============================================================
#
# Escribir Parquet NO es "guardar un archivo".
#
# Es:
# - Diseñar cómo vivirán tus datos
# - Decidir cómo se leerán mañana
# - Evitar errores futuros
#
# ============================================================


if __name__ == "__main__":
    ejemplo_completo()
