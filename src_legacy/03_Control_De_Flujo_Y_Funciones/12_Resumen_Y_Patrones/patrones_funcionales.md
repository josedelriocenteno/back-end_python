# Patrones Funcionales en Python para Backend y Data

## 1. Guard Clauses / Early Return
Evita anidamientos excesivos comprobando condiciones al inicio de la función.

```python
def process_user(user):
    if not user.get("active"):
        return None
    return user["name"]
Uso: endpoints, validación de datos.

2. Comprehensions
List, dict y set comprehensions para transformar colecciones de forma clara.

python
Copiar código
# List
squared = [x**2 for x in range(10) if x % 2 == 0]

# Dict
user_age = {u["name"]: u["age"] for u in users if u["age"] > 18}

# Set
unique_ages = {u["age"] for u in users}
Uso: filtrado, transformación, limpieza de datos.

3. Funciones Puras
Funciones deterministas, sin efectos secundarios.

python
Copiar código
def square(x: int) -> int:
    return x**2
Uso: testabilidad, pipelines de transformación.

4. Closures
Funciones que recuerdan estado para contadores, validadores o factories.

python
Copiar código
def make_multiplier(factor):
    def multiply(n):
        return n * factor
    return multiply

doubler = make_multiplier(2)
Uso: contadores, configuraciones dinámicas.

5. Decorators
Reutilización de lógica transversal: logging, caching, timing, auth.

python
Copiar código
from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} tardó {time.time()-start:.4f}s")
        return result
    return wrapper
Uso: medir rendimiento de endpoints, pipelines.

6. Funciones de Orden Superior
map, filter, reduce para aplicar transformaciones funcionales.

python
Copiar código
from functools import reduce

nums = [1,2,3,4]
squared = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x%2==0, nums))
total = reduce(lambda a,b: a+b, nums)
Uso: pipelines de datos y procesamiento batch.

7. Tipado y Docstrings
Aumenta claridad y mantenibilidad.

python
Copiar código
def divide(a: float, b: float) -> float:
    """
    Divide a entre b
    Raises ValueError if b==0
    """
    if b == 0:
        raise ValueError("División entre cero")
    return a / b
Uso: APIs, librerías internas, colaboración profesional.

8. Funciones Inmutables
Evita mutar datos para mejorar seguridad y predictibilidad.

python
Copiar código
def append_immutable(lst, val):
    return lst + [val]
Uso: pipelines de datos, concurrencia segura.

9. Idempotencia
Funciones que pueden ejecutarse múltiples veces sin cambiar el resultado.

python
Copiar código
def normalize_user(user: dict) -> dict:
    user["name"] = user["name"].strip().lower()
    return user
Uso: endpoints REST, procesamiento batch.

10. Patrones Combinados en Pipelines
Integra todos los patrones anteriores en pipelines profesionales.

python
Copiar código
def process_users(users):
    @timer
    def clean(user):
        if "name" not in user or user.get("age", 0)<=0:
            return None
        return {**user, "name": user["name"].strip().lower()}

    return [clean(u) for u in users if clean(u)]
Uso: backend profesional, data engineering, ML preprocessing.

✅ Buenas prácticas generales
Mantén funciones puras siempre que sea posible.

Prefiere closures a variables globales.

Usa decorators para lógica transversal.

Documenta siempre con docstrings y tipado.

Evita bucles complejos usando comprehensions y funciones de orden superior.

Integra logging y control de errores de forma consistente.