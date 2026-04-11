# resumen_control_flujo.py
"""
RESUMEN DE CONTROL DE FLUJO Y FUNCIONES EN PYTHON
=================================================

Objetivo:
- Tener un repaso rápido y profesional de toda la unidad
- Orientación a backend, pipelines de datos y buenas prácticas
- Incluye ejemplos claros y patrones reutilizables
"""

# =========================================================
# 1. Control de flujo básico
# =========================================================

# Condicionales
x = 10
if x > 0:
    print("Positivo")
elif x == 0:
    print("Cero")
else:
    print("Negativo")

# Guard clauses / early return
def process_user(user):
    if not user.get("active"):
        return None  # evita anidamientos
    return user["name"]

# =========================================================
# 2. Bucles
# =========================================================

# For clásico
for i in range(5):
    print(i)

# While
count = 0
while count < 5:
    print(count)
    count += 1

# Enumerate y zip
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 22]
for i, (name, age) in enumerate(zip(names, ages)):
    print(i, name, age)

# Break / Continue / Pass
for i in range(10):
    if i % 2 == 0:
        continue  # salta pares
    elif i == 7:
        break     # sale del bucle
    else:
        pass      # placeholder

# =========================================================
# 3. Comprensiones
# =========================================================

# List comprehension
squared = [x**2 for x in range(5)]

# Dict comprehension
age_dict = {name: age for name, age in zip(names, ages)}

# Set comprehension
unique_ages = {age for age in ages}

# =========================================================
# 4. Funciones básicas
# =========================================================

def suma(a: int, b: int) -> int:
    """Suma dos números enteros"""
    return a + b

# Parámetros con valores por defecto
def greet(name: str = "Guest") -> str:
    return f"Hello, {name}!"

# Funciones puras
def square(x: int) -> int:
    return x**2

# =========================================================
# 5. Funciones avanzadas
# =========================================================

# *args y **kwargs
def log(message: str, *args, **kwargs):
    print(message, args, kwargs)

# Keyword-only args
def connect(*, host: str, port: int):
    print(f"Connecting to {host}:{port}")

# Type hints
def multiply(x: int, y: int) -> int:
    return x * y

# Docstrings profesionales
def divide(a: float, b: float) -> float:
    """
    Divide a entre b
    Args:
        a (float): Numerador
        b (float): Denominador
    Returns:
        float: Resultado de la división
    Raises:
        ValueError: Si b == 0
    """
    if b == 0:
        raise ValueError("División entre cero")
    return a / b

# =========================================================
# 6. Scope y lifetime
# =========================================================

x_global = 100  # global

def scope_example():
    x_local = 10  # local
    def inner():
        nonlocal x_local
        x_local += 5
        return x_local
    return inner()

# =========================================================
# 7. Closures
# =========================================================

def make_multiplier(factor):
    """Closure que multiplica por un factor"""
    def multiply(n):
        return n * factor
    return multiply

doubler = make_multiplier(2)
tripler = make_multiplier(3)

# =========================================================
# 8. Decorators
# =========================================================

from functools import wraps
import time

def timer(func):
    """Decorator que mide tiempo de ejecución"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} tardó {end-start:.4f} segundos")
        return result
    return wrapper

@timer
def compute():
    return sum(i**2 for i in range(1000))

# =========================================================
# 9. Funciones en backend y pipelines
# =========================================================

def clean_user_data(user: dict) -> dict:
    """Transformación de datos: limpiar nombres y validar edad"""
    if not isinstance(user.get("edad"), int) or user.get("edad") <= 0:
        return {}
    user["nombre"] = user["nombre"].strip().lower()
    return user

# Funciones idempotentes
def square_list(numbers: list[int]) -> list[int]:
    return [x**2 for x in numbers]

# =========================================================
# 10. Funcional en Python
# =========================================================

# map, filter, reduce
from functools import reduce

nums = [1, 2, 3, 4]
squared_nums = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))
sum_total = reduce(lambda a, b: a + b, nums)

# Funciones inmutables
def append_immutable(lst: list[int], val: int) -> list[int]:
    return lst + [val]
