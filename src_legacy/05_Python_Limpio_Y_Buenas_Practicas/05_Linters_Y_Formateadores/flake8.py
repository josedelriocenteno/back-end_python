"""
flake8.py
=========

Este archivo explica cómo usar Flake8 para detectar errores de estilo y problemas comunes
en Python, siguiendo las buenas prácticas de PEP8 y clean code.

Flake8 combina:
- pyflakes: detecta errores lógicos y sintácticos
- pycodestyle: verifica PEP8 (espacios, indentación, nombres, líneas)
- mccabe: analiza complejidad ciclomática de funciones
"""

# -------------------------------------------------------------------
# 1️⃣ INSTALACIÓN
# -------------------------------------------------------------------

# Desde terminal:
# pip install flake8

# Para comprobar versión:
# flake8 --version

# Para analizar un archivo específico:
# flake8 mi_archivo.py

# Para analizar todo el proyecto:
# flake8 src/ tests/ --max-line-length=88


# -------------------------------------------------------------------
# 2️⃣ ERRORES DE ESTILO COMUNES DETECTADOS POR FLAKE8
# -------------------------------------------------------------------

# ❌ MAL: líneas muy largas, mal indentadas y espacios inconsistentes
def funcion_mala():  # noqa: solo ejemplo
    x= 10; y=20;z= x+y;print(z)  

# ❌ MAL: nombre de variable poco profesional
def f(a,b):
  return a+b

# ✅ BIEN: estilo limpio según PEP8 y Flake8
def sumar(a: int, b: int) -> int:
    """
    Suma dos números enteros.

    Args:
        a (int): Primer número.
        b (int): Segundo número.

    Returns:
        int: Suma de a y b.
    """
    resultado = a + b
    return resultado


# -------------------------------------------------------------------
# 3️⃣ ERRORES DE LÓGICA DETECTABLES
# -------------------------------------------------------------------

# ❌ MAL: asignación inútil
def calcular_total_mal(productos: list[dict]) -> float:
    total = 0
    for p in productos:
        total = total  # Flake8 / Pyflakes alerta: asignación inútil
        total += p["precio"]
    return total

# ❌ MAL: variable sin usar
def dividir(a: float, b: float) -> float:
    resultado = a / b
    return b  # Flake8 detecta variable sin usar: resultado

# ✅ BIEN: corregido
def calcular_total(productos: list[dict]) -> float:
    total = sum(p["precio"] for p in productos)
    return total


# -------------------------------------------------------------------
# 4️⃣ COMPLEJIDAD CICLOMÁTICA
# -------------------------------------------------------------------

# ❌ MAL: función demasiado compleja
def procesar_pedido_complejo(pedido: dict) -> float:
    total = 0
    if pedido.get("productos"):
        for p in pedido["productos"]:
            if p.get("disponible"):
                if p.get("precio", 0) > 0:
                    if pedido.get("usuario") and pedido["usuario"].get("activo"):
                        total += p["precio"]
    return total

# Flake8 + mccabe alertan sobre complejidad > 10
# ✅ BIEN: refactorizando en funciones pequeñas y guard clauses
def producto_valido(p: dict, usuario: dict) -> bool:
    return p.get("disponible", False) and p.get("precio", 0) > 0 and usuario.get("activo", False)

def procesar_pedido(pedido: dict) -> float:
    usuario = pedido.get("usuario", {})
    total = sum(p["precio"] for p in pedido.get("productos", []) if producto_valido(p, usuario))
    return total


# -------------------------------------------------------------------
# 5️⃣ INTEGRACIÓN EN EL PROYECTO
# -------------------------------------------------------------------

# Configurar Flake8 con archivo pyproject.toml o setup.cfg:
#
# [flake8]
# max-line-length = 88
# extend-ignore = E203,W503
# exclude = .git,__pycache__,venv

# Ejecutar automáticamente antes de commit usando pre-commit
# git init
# pip install pre-commit
# pre-commit install

# Esto asegura que TODO el código que subas cumple con PEP8 y evita errores simples


# -------------------------------------------------------------------
# 6️⃣ REGLAS DE ORO
# -------------------------------------------------------------------

# 1. Corrige warnings de Flake8 antes de hacer commit
# 2. Usa nombres claros, espacios correctos, indentación consistente
# 3. Evita líneas demasiado largas (>88 caracteres)
# 4. Evita variables no usadas o asignaciones inútiles
# 5. Mantén funciones pequeñas y simples
# 6. Revisa complejidad ciclomática (mccabe) para funciones críticas


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------

# Flake8 + pre-commit = primer filtro de calidad
# Reduce errores simples, mantiene consistencia y mejora profesionalidad
# Fundamental en proyectos backend y pipelines de IA
