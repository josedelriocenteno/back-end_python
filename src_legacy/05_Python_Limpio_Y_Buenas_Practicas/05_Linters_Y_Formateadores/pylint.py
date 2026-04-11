"""
pylint.py
=========

Este archivo enseña cómo usar Pylint para análisis estático de código Python,
detectando errores, malas prácticas, complejidad y estilo.

Diferencias clave con Flake8:
- Pylint es más estricto y detallado
- Proporciona puntuación global del código (0-10)
- Detecta errores lógicos, convenciones, docstrings faltantes y código muerto
"""

# -------------------------------------------------------------------
# 1️⃣ INSTALACIÓN
# -------------------------------------------------------------------

# pip install pylint

# Para revisar un archivo:
# pylint mi_archivo.py

# Para obtener puntuación global:
# pylint mi_archivo.py --score=y


# -------------------------------------------------------------------
# 2️⃣ EJEMPLOS DE ERRORES DETECTADOS POR PYLINT
# -------------------------------------------------------------------

# ❌ MAL: variable sin usar
def dividir(a: float, b: float) -> float:
    resultado = a / b
    return b  # Pylint alerta: variable 'resultado' asignada pero no usada

# ❌ MAL: clase sin docstring
class ProductoMalo:
    pass  # Pylint alerta: clase sin docstring

# ❌ MAL: función sin docstring
def foo():
    return 42  # Pylint alerta: función sin docstring

# ❌ MAL: nombres poco profesionales
x = 10
def f(a,b):
    return a+b  # Pylint alerta sobre nombres poco descriptivos


# -------------------------------------------------------------------
# 3️⃣ CORRECCIÓN CON PYLINT EN MENTE
# -------------------------------------------------------------------

# ✅ BIEN: nombres claros, docstrings, tipado
def dividir_segura(a: float, b: float) -> float:
    """
    Divide `a` entre `b`.

    Args:
        a (float): Dividendo.
        b (float): Divisor.

    Returns:
        float: Resultado de la división.

    Raises:
        ValueError: Si `b` es 0.
    """
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b


class Producto:
    """
    Representa un producto en la tienda.

    Attributes:
        id (int): Identificador único.
        nombre (str): Nombre del producto.
        precio (float): Precio en USD.
    """
    def __init__(self, id: int, nombre: str, precio: float):
        self.id = id
        self.nombre = nombre
        self.precio = precio


# -------------------------------------------------------------------
# 4️⃣ COMPLEJIDAD Y LONGITUD
# -------------------------------------------------------------------

# ❌ MAL: función gigante con muchas ramas
def procesar_pedido(pedido: dict) -> float:
    total = 0
    if pedido.get("productos"):
        for p in pedido["productos"]:
            if p.get("disponible"):
                if p.get("precio", 0) > 0:
                    if pedido.get("usuario") and pedido["usuario"].get("activo"):
                        total += p["precio"]
    return total

# ✅ BIEN: separar en funciones pequeñas
def producto_valido(p: dict, usuario: dict) -> bool:
    return p.get("disponible", False) and p.get("precio", 0) > 0 and usuario.get("activo", False)

def calcular_total_pedido(pedido: dict) -> float:
    usuario = pedido.get("usuario", {})
    return sum(p["precio"] for p in pedido.get("productos", []) if producto_valido(p, usuario))


# -------------------------------------------------------------------
# 5️⃣ INTEGRACIÓN EN EL PROYECTO
# -------------------------------------------------------------------

# Configuración recomendada (pylintrc):
#
# [MASTER]
# ignore=venv
# max-line-length=88
#
# [MESSAGES CONTROL]
# disable=C0114,C0115,C0116  # opcional: deshabilita docstring warnings si ya tienes otra convención
#
# [REPORTS]
# output-format=colorized
# score=yes

# Se puede integrar en pre-commit para revisión automática
# pip install pre-commit
# pre-commit install


# -------------------------------------------------------------------
# 6️⃣ REGLAS DE ORO
# -------------------------------------------------------------------

# 1. Siempre documenta clases y funciones (docstrings)
# 2. Nombres claros y descriptivos
# 3. Mantén funciones pequeñas y lineales
# 4. Evita variables sin usar y asignaciones inútiles
# 5. Mantén complejidad ciclomática baja
# 6. Configura pylint y pre-commit para revisión automática


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------

# Pylint = herramienta estricta de control de calidad
# Detecta problemas que Flake8 puede no cubrir
# Fundamental para proyectos profesionales y producción
# Combinar Flake8 + Pylint + pre-commit = calidad máxima
