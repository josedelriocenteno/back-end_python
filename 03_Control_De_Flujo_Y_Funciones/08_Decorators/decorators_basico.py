# decorators_basico.py
"""
DECORATORS BÁSICOS EN PYTHON
============================

Objetivo:
- Entender qué es un decorator y cómo funciona realmente
- Aprender a aplicarlo en backend, APIs y pipelines de datos
- Mantener código limpio, reutilizable y profesional
"""

# =========================================================
# 1. Concepto clave
# =========================================================
# Un decorator es una función que recibe otra función y devuelve otra función,
# normalmente extendiendo o modificando el comportamiento de la original.
# Se usa mucho para logging, autorización, validaciones, caching, métricas.

# =========================================================
# 2. Ejemplo básico
# =========================================================

def decorador_simple(func):
    """Decorator que imprime antes y después de ejecutar la función"""
    def wrapper(*args, **kwargs):
        print(f"Antes de {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"Después de {func.__name__}")
        return resultado
    return wrapper

@decorador_simple
def saludar(nombre):
    print(f"Hola {nombre}")

saludar("Carlos")
# Salida:
# Antes de saludar
# Hola Carlos
# Después de saludar

# =========================================================
# 3. Decorator sin sintaxis @
# =========================================================

def sumar(a, b):
    return a + b

decorado = decorador_simple(sumar)
print(decorado(5, 7))
# Antes de wrapper
# Después de wrapper
# 12

# =========================================================
# 4. Decorators con parámetros
# =========================================================

def repetir_veces(n):
    """Decorator que ejecuta la función n veces"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                print(f"Iteración {i+1}")
                func(*args, **kwargs)
        return wrapper
    return decorator

@repetir_veces(3)
def saludo(nombre):
    print(f"Hola {nombre}")

saludo("Ana")
# Iteración 1 -> Hola Ana
# Iteración 2 -> Hola Ana
# Iteración 3 -> Hola Ana

# =========================================================
# 5. Uso profesional en backend
# =========================================================

# Logging en endpoints
def log_endpoint(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Llamando endpoint {func.__name__} con args={args} kwargs={kwargs}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] Endpoint {func.__name__} devolvió {resultado}")
        return resultado
    return wrapper

@log_endpoint
def procesar_datos(data):
    # Simula procesamiento de datos
    return {k: v*2 for k, v in data.items()}

procesar_datos({"a": 1, "b": 2})
# [LOG] Llamando endpoint procesar_datos con args=({'a':1,'b':2},) kwargs={}
# [LOG] Endpoint procesar_datos devolvió {'a':2,'b':4}

# =========================================================
# 6. Buenas prácticas
# =========================================================
# - Usar functools.wraps(func) para preservar metadata de la función original
# - Documentar qué hace cada decorator
# - Evitar side effects complejos dentro del decorator
# - Usar decorators para:
#   - Logging y métricas
#   - Validaciones y auth
#   - Caching y memoization
#   - Reintentos y control de errores
