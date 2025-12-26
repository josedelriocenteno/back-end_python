# decorators_con_parametros.py
"""
DECORATORS CON PARÁMETROS EN PYTHON
===================================

Objetivo:
- Crear decorators que acepten argumentos de configuración
- Aplicación en backend, logging, validación de APIs y pipelines
- Mantener código limpio, reutilizable y testable
"""

from functools import wraps

# =========================================================
# 1. Concepto
# =========================================================
# Un decorator con parámetros es una función que devuelve un decorator.
# Es decir, se necesitan 3 niveles de funciones:
#   1. Función exterior: recibe parámetros del decorator
#   2. Función intermedia: recibe la función a decorar
#   3. Wrapper: reemplaza la función original y añade funcionalidad

# =========================================================
# 2. Ejemplo básico: repetir n veces
# =========================================================

def repetir_veces(n: int):
    """Decorator configurable que ejecuta la función n veces"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(n):
                print(f"[Iteración {i+1}]")
                func(*args, **kwargs)
        return wrapper
    return decorator

@repetir_veces(3)
def saludo(nombre):
    print(f"Hola {nombre}")

saludo("Ana")
# Output:
# [Iteración 1] -> Hola Ana
# [Iteración 2] -> Hola Ana
# [Iteración 3] -> Hola Ana

# =========================================================
# 3. Decorator profesional: logging con nivel
# =========================================================

def log_con_nivel(nivel: str = "INFO"):
    """Decorator configurable para logging de funciones"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{nivel}] Llamando {func.__name__} con args={args} kwargs={kwargs}")
            resultado = func(*args, **kwargs)
            print(f"[{nivel}] {func.__name__} devolvió {resultado}")
            return resultado
        return wrapper
    return decorator

@log_con_nivel("DEBUG")
def procesar_datos(data: dict):
    return {k: v*2 for k, v in data.items()}

procesar_datos({"x": 1, "y": 2})
# [DEBUG] Llamando procesar_datos con args=({'x':1,'y':2},) kwargs={}
# [DEBUG] procesar_datos devolvió {'x':2,'y':4}

# =========================================================
# 4. Decorator configurable para validación
# =========================================================

def validar_edad(min_edad: int):
    """Decorator que valida la edad antes de ejecutar la función"""
    def decorator(func):
        @wraps(func)
        def wrapper(edad, *args, **kwargs):
            if edad < min_edad:
                raise ValueError(f"La edad debe ser >= {min_edad}")
            return func(edad, *args, **kwargs)
        return wrapper
    return decorator

@validar_edad(18)
def registrar_usuario(edad, nombre):
    print(f"Usuario registrado: {nombre}, edad {edad}")

registrar_usuario(20, "Carlos")  # Funciona
# registrar_usuario(16, "Ana")  # ValueError

# =========================================================
# 5. Buenas prácticas
# =========================================================
# - Siempre usar functools.wraps para preservar metadata
# - Documentar claramente los parámetros del decorator
# - Mantener la lógica del wrapper simple y clara
# - Separar responsabilidades: un decorator hace solo una cosa
# - Ideal para:
#   - Logging configurable
#   - Validaciones de entrada con parámetros
#   - Retries y timeouts ajustables
#   - Caching con parámetros (ej: TTL)
