"""
evitar_side_effects.py
======================

Buenas prácticas: evitar side effects / usar funciones puras

Objetivos:
- Escribir funciones puras para reproducibilidad
- Separar efectos secundarios de la lógica principal
- Facilitar testeo y mantenimiento
"""

# -------------------------------------------------------------------
# 1️⃣ ¿QUÉ ES UN SIDE EFFECT?
# -------------------------------------------------------------------

# Side effect (efecto secundario): cualquier acción que cambia el estado
# fuera de la función o tiene interacción externa:
# - Modificar variables globales
# - Escribir archivos
# - Imprimir en consola
# - Modificar argumentos mutables directamente
# - Acceder a DB o APIs externas

# Función con side effect
contador_global = 0

def sumar_con_side_effect(a, b):
    global contador_global
    contador_global += 1  # ❌ modifica estado externo
    return a + b

# Problemas:
# - Difícil de testear (depende de contador_global)
# - No reproducible: misma entrada puede dar resultados distintos


# -------------------------------------------------------------------
# 2️⃣ FUNCIONES PURAS
# -------------------------------------------------------------------

# Características:
# 1. Siempre devuelve el mismo output para los mismos inputs
# 2. No modifica estado externo
# 3. No tiene efectos secundarios ocultos

def sumar_pura(a, b):
    """Función pura: predecible y testable"""
    return a + b

def filtrar_mayores(df, umbral):
    """
    Función pura: devuelve un nuevo DataFrame sin modificar el original
    """
    df_nuevo = df.copy()
    return df_nuevo[df_nuevo["valor"] > umbral]


# -------------------------------------------------------------------
# 3️⃣ SEPARAR EFECTOS SECUNDARIOS
# -------------------------------------------------------------------

# Buen patrón: mantener side effects fuera de la lógica
def procesar_datos(df):
    """
    Lógica pura: transforma datos sin side effects
    """
    df = df.copy()
    df["total"] = df["cantidad"] * df["precio_unitario"]
    return df

def guardar_datos(df, ruta):
    """
    Efecto secundario separado: persistencia
    """
    df.to_csv(ruta, index=False)

def imprimir_resumen(df):
    """
    Efecto secundario separado: reporting
    """
    print(df.describe())


# -------------------------------------------------------------------
# 4️⃣ PIPELINE LIMPIO USANDO FUNCIONES PURAS
# -------------------------------------------------------------------

def pipeline_limpio_sin_side_effects(df, ruta_salida=None):
    """
    Orquesta pipeline limpio: pura lógica + efectos separados
    """
    df_procesado = procesar_datos(df)  # pura
    if ruta_salida:
        guardar_datos(df_procesado, ruta_salida)  # side effect separado
    imprimir_resumen(df_procesado)  # side effect separado
    return df_procesado


# -------------------------------------------------------------------
# 5️⃣ BENEFICIOS DE FUNCIONES PURAS
# -------------------------------------------------------------------

# 1. Testables: se puede testear sin mocks
# 2. Reproducibles: mismos inputs → mismos outputs
# 3. Componibles: se pueden combinar pipelines fácilmente
# 4. Mantener side effects separados mejora legibilidad
# 5. Reduce errores difíciles de depurar


# -------------------------------------------------------------------
# 6️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Principios clave:
# - Funciones puras siempre que sea posible
# - Side effects separados y controlados
# - Reproducibilidad y testabilidad = clean code en Data/ML
