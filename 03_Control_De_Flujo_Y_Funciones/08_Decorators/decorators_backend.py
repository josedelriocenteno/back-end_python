# decorators_backend.py
"""
DECORATORS EN BACKEND: AUTH, LOGGING, CACHING Y TIMING
======================================================

Objetivo:
- Aplicar decorators a funciones críticas de backend
- Mejorar seguridad, rendimiento, trazabilidad y mantenibilidad
- Mantener código limpio, testable y reutilizable
"""

from functools import wraps
import time
from typing import Callable, Any

# =========================================================
# 1. Decorator de logging profesional
# =========================================================
def log_backend(func: Callable) -> Callable:
    """Logger simple para funciones de backend"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Llamando a {func.__name__} con args={args}, kwargs={kwargs}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} devolvió {resultado}")
        return resultado
    return wrapper

# Uso
@log_backend
def obtener_usuario(id_usuario: int) -> dict:
    return {"id": id_usuario, "nombre": "Ana"}

# =========================================================
# 2. Decorator de autorización (Auth)
# =========================================================
def requiere_rol(rol: str):
    """Decorator que simula autorización por roles"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(usuario: dict, *args, **kwargs):
            if usuario.get("rol") != rol:
                raise PermissionError(f"Se requiere el rol '{rol}'")
            return func(usuario, *args, **kwargs)
        return wrapper
    return decorator

# Uso
@requiere_rol("admin")
def eliminar_usuario(usuario: dict, id_usuario: int):
    print(f"Usuario {id_usuario} eliminado por {usuario['nombre']}")

# =========================================================
# 3. Decorator de caching simple
# =========================================================
def cache_resultados(func: Callable) -> Callable:
    """Caching simple en memoria (no distribuido)"""
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print("[CACHE] Resultado recuperado")
            return cache[args]
        resultado = func(*args)
        cache[args] = resultado
        return resultado
    return wrapper

@cache_resultados
def calcular_valor(x: int, y: int) -> int:
    print("Calculando...")
    return x + y

# =========================================================
# 4. Decorator de timing para medir rendimiento
# =========================================================
def medir_tiempo(func: Callable) -> Callable:
    """Mide tiempo de ejecución de funciones"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"[TIMING] {func.__name__} tardó {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

@medir_tiempo
def procesar_datos_largos(n: int):
    return sum(i**2 for i in range(n))

# =========================================================
# 5. Buenas prácticas
# =========================================================
# - Separar responsabilidades: un decorator hace solo una cosa
# - Encadenar decorators de forma lógica (auth -> logging -> timing)
# - Usar functools.wraps para preservar metadata
# - Evitar lógica compleja dentro del wrapper: delegar a funciones auxiliares
# - Ideal para:
#   - Endpoints de APIs
#   - Funciones de pipelines de datos
#   - Servicios críticos que requieren trazabilidad y seguridad
