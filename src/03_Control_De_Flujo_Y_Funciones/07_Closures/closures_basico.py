# closures_basico.py
"""
CLOSURES EN PYTHON
==================

Objetivo:
- Entender qué es un closure y cómo funciona en Python
- Usarlos para mantener estado sin usar variables globales
- Aplicación práctica en backend, APIs y pipelines de datos

Conceptos clave:
- Closure: función que recuerda variables de su scope externo, incluso después de que el scope externo haya terminado.
- Permite encapsular estado de manera segura y limpia.
- Evita uso de variables globales y mejora testabilidad.
"""

# =========================================================
# 1. Ejemplo básico de closure
# =========================================================

def contador():
    n = 0  # variable de enclosing scope

    def incrementar():
        nonlocal n  # recordar que n viene de la función externa
        n += 1
        return n

    return incrementar  # retornamos la función, no su valor

c = contador()  # crea un closure
print(c())  # 1
print(c())  # 2
print(c())  # 3

# Cada llamada recuerda el valor anterior de n sin usar global

# =========================================================
# 2. Closures con parámetros
# =========================================================

def multiplicador(factor):
    """Crea una función que multiplica por un factor fijo"""
    def multiplicar(x):
        return x * factor
    return multiplicar

por_3 = multiplicador(3)
print(por_3(10))  # 30
print(por_3(7))   # 21

por_5 = multiplicador(5)
print(por_5(10))  # 50

# =========================================================
# 3. Aplicación en backend/pipelines
# =========================================================

def pipeline_logger(stage_name):
    """Closure para llevar cuenta de invocaciones de un stage en un pipeline"""
    contador_stage = 0

    def log_stage(data):
        nonlocal contador_stage
        contador_stage += 1
        print(f"[{stage_name}] llamada #{contador_stage} con datos: {data}")
        return data  # normalmente aquí se haría transformación real

    return log_stage

stage_a = pipeline_logger("ETL Stage A")
stage_a({"id": 1})  # [ETL Stage A] llamada #1 con datos: {'id': 1}
stage_a({"id": 2})  # [ETL Stage A] llamada #2 con datos: {'id': 2}

# =========================================================
# 4. Buenas prácticas
# =========================================================
# - Documentar claramente qué variables se están capturando
# - Usar closures para encapsular estado que no debe ser global
# - No abusar de closures en pipelines muy largos; considerar clases si el estado es complejo
# - Evitar modificar objetos mutables desde closures si quieres inmutabilidad
# - Ideal para logging, contadores, validadores y factories
