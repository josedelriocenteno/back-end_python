# errores_decorators_comunes.py
"""
ERRORES COMUNES EN DECORATORS
==============================

Objetivo:
- Identificar errores típicos al crear decorators en Python
- Aprender cómo evitarlos para mantener código limpio, seguro y testable
- Orientado a backend, APIs y pipelines de datos
"""

from functools import wraps
import time

# =========================================================
# 1. No usar functools.wraps
# =========================================================
def decorador_incorrecto(func):
    """Decorator sin wraps pierde metadata"""
    def wrapper(*args, **kwargs):
        print("Ejecutando función...")
        return func(*args, **kwargs)
    return wrapper

@decorador_incorrecto
def ejemplo():
    """Documentación perdida"""
    return 42

print(ejemplo.__name__)  # -> wrapper (PERDIDA DE METADATA)
print(ejemplo.__doc__)   # -> None

# CORRECTO:
def decorador_correcto(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# =========================================================
# 2. Modificar argumentos o resultados sin cuidado
# =========================================================
def decorador_peligroso(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Error: modificar args mutable directamente
        for i, a in enumerate(args):
            if isinstance(a, list):
                a.append("modificado")  # afecta fuera del scope
        return func(*args, **kwargs)
    return wrapper

# =========================================================
# 3. Decorator con lógica pesada
# =========================================================
def decorador_lento(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Mala práctica: mucho cálculo dentro del decorator
        for _ in range(10**6):
            pass
        return func(*args, **kwargs)
    return wrapper

# Consecuencia: afecta a todas las llamadas, incluso si no siempre se necesita

# =========================================================
# 4. No manejar excepciones dentro del decorator
# =========================================================
def decorador_riesgoso(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Error: cualquier excepción rompe el flujo
        resultado = func(*args, **kwargs)
        return resultado + 1  # si func devuelve string, explota
    return wrapper

# =========================================================
# 5. Decorators que dependen de estado global mutable
# =========================================================
contador_global = 0

def decorador_global(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global contador_global
        contador_global += 1  # puede causar condiciones de carrera
        return func(*args, **kwargs)
    return wrapper

# =========================================================
# 6. Buenas prácticas para evitar errores
# =========================================================
# - Usar functools.wraps siempre
# - No modificar argumentos mutables directamente
# - Mantener lógica ligera dentro del wrapper
# - Manejar errores y validar entradas
# - Evitar dependencias globales o estados compartidos
# - Documentar claramente el comportamiento del decorator

# =========================================================
# 7. Consejos profesionales
# =========================================================
# - Encadenar decorators de forma lógica
# - Testear cada decorator individualmente
# - Usar decorators para cross-cutting concerns: logging, auth, caching, timing
# - Evitar decorar funciones críticas sin pruebas
