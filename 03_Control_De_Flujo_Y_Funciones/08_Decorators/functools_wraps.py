# functools_wraps.py
"""
FUNCTOOLS.WRAP EN DECORATORS
=============================

Objetivo:
- Entender qué es functools.wraps y por qué es crítico en decorators
- Evitar perder metadata de la función original
- Mantener compatibilidad con introspección, documentación y testing
"""

from functools import wraps

# =========================================================
# 1. Problema sin functools.wraps
# =========================================================
def decorador_simple(func):
    """Decorator que no preserva metadata"""
    def wrapper(*args, **kwargs):
        print("Ejecutando función decorada...")
        return func(*args, **kwargs)
    return wrapper

@decorador_simple
def saludar(nombre):
    """Función que saluda a alguien"""
    print(f"Hola {nombre}")

print(saludar.__name__)  # wrapper
print(saludar.__doc__)   # None o doc del wrapper

# Observa que __name__, __doc__ y otras propiedades se pierden
# Esto es un problema para debugging, logging y frameworks que inspeccionan funciones

# =========================================================
# 2. Solución con functools.wraps
# =========================================================
def decorador_correcto(func):
    """Decorator que preserva metadata usando functools.wraps"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Ejecutando función decorada correctamente...")
        return func(*args, **kwargs)
    return wrapper

@decorador_correcto
def saludar(nombre):
    """Función que saluda a alguien"""
    print(f"Hola {nombre}")

print(saludar.__name__)  # saludar
print(saludar.__doc__)   # Función que saluda a alguien

# =========================================================
# 3. Uso profesional
# =========================================================
# - Logging en endpoints:
def log_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Llamando {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} devolvió {resultado}")
        return resultado
    return wrapper

# - Decorators de validación en APIs:
def validar_parametros(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Validando parámetros de {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# =========================================================
# 4. Buenas prácticas
# =========================================================
# - Siempre envolver el wrapper con @wraps(func)
# - Facilita introspección, logging, debugging, testing y documentación automática
# - Fundamental cuando se usan decorators en:
#   - APIs REST/GraphQL
#   - Pipelines de datos
#   - Funciones críticas de backend
# - Evita errores difíciles de detectar en frameworks que inspeccionan funciones
