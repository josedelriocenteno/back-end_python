"""
pipelines_limpios.py
====================

Buenas prácticas: pipelines limpios de datos y ML

Objetivos:
- Código reproducible y mantenible
- Separar etapas claramente
- Evitar side effects innecesarios
- Facilitar testeo y debug
"""

# -------------------------------------------------------------------
# 1️⃣ PROBLEMA: PIPELINES SUCIOS
# -------------------------------------------------------------------

# ❌ MAL: funciones que hacen todo a la vez
def pipeline_sucio(ruta_csv: str):
    import pandas as pd
    df = pd.read_csv(ruta_csv)  # leer datos
    df = df.dropna()            # limpiar
    df["precio_total"] = df["cantidad"] * df["precio_unitario"]  # feature
    df.to_csv("salida.csv")     # guardar
    print(df.describe())        # imprimir resumen
    return df

# Problemas:
# 1. Difícil de testear cada etapa
# 2. Mezcla lectura, limpieza, transformación, almacenamiento y reporting
# 3. No reproducible: resultados dependen de side effects (guardar, imprimir)
# 4. Difícil de mantener y extender


# -------------------------------------------------------------------
# 2️⃣ SOLUCIÓN: PIPELINE LIMPIO Y REPRODUCIBLE
# -------------------------------------------------------------------

import pandas as pd
from typing import Optional

# Función para lectura de datos
def cargar_datos(ruta_csv: str) -> pd.DataFrame:
    """Carga datos desde CSV y devuelve DataFrame limpio de NaNs"""
    df = pd.read_csv(ruta_csv)
    return df.dropna()

# Función de transformación
def agregar_feature_precio_total(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columna de precio total"""
    df = df.copy()  # evita modificar df original
    df["precio_total"] = df["cantidad"] * df["precio_unitario"]
    return df

# Función para filtrado opcional
def filtrar_por_categoria(df: pd.DataFrame, categoria: Optional[str] = None) -> pd.DataFrame:
    """Filtra por categoría si se proporciona"""
    if categoria:
        return df[df["categoria"] == categoria]
    return df

# Función de salida (sin efectos secundarios en pipeline principal)
def guardar_salida(df: pd.DataFrame, ruta_salida: Optional[str] = None):
    """Guarda DataFrame a CSV si se proporciona ruta"""
    if ruta_salida:
        df.to_csv(ruta_salida, index=False)

# Función de reporting (separada)
def imprimir_resumen(df: pd.DataFrame):
    """Imprime resumen estadístico de los datos"""
    print(df.describe())


# -------------------------------------------------------------------
# 3️⃣ PIPELINE ORQUESTADOR
# -------------------------------------------------------------------

def pipeline_limpio(ruta_csv: str, ruta_salida: Optional[str] = None, categoria: Optional[str] = None) -> pd.DataFrame:
    """
    Orquesta pipeline de datos limpio y reproducible
    """
    df = cargar_datos(ruta_csv)
    df = agregar_feature_precio_total(df)
    df = filtrar_por_categoria(df, categoria)
    guardar_salida(df, ruta_salida)
    imprimir_resumen(df)
    return df


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS
# -------------------------------------------------------------------

# 1. Cada función hace solo una cosa (SRP)
# 2. Fácil de testear individualmente:
#    - cargar_datos()
#    - agregar_feature_precio_total()
#    - filtrar_por_categoria()
# 3. Reproducible: resultados no dependen de side effects internos
# 4. Pipeline modular: fácil añadir nuevas transformaciones
# 5. Legible y mantenible


# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Principios clave para pipelines limpios:
# - Separar lectura, limpieza, transformación, almacenamiento y reporting
# - Evitar efectos secundarios ocultos
# - Usar funciones puras siempre que sea posible
# - Orquestar todo en función principal clara
# - Código modular = reproducible, testable y profesional
