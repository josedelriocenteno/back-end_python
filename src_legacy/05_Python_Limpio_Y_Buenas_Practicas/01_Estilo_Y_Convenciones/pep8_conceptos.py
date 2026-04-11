"""
pep8_conceptos.py
=================

Este archivo introduce PEP 8, la guía oficial de estilo en Python.

PEP 8 NO es una moda.
PEP 8 es un contrato social:
- para que el código sea legible
- para que los equipos trabajen sin fricción
- para que las herramientas automáticas funcionen

Ignorar PEP 8 en proyectos reales NO es neutral:
es una señal de falta de profesionalidad.
"""

# -------------------------------------------------------------------
# 1️⃣ ESPACIOS Y SANGRADO (INDENTATION)
# -------------------------------------------------------------------
#
# Python usa la indentación para definir bloques de código.
# No es estética: es SINTAXIS.
#
# Regla:
# - 4 espacios por nivel
# - NUNCA mezclar tabs y espacios

# ❌ MAL
def funcion_mal_indentada():
  x = 10
  if x > 5:
    print("esto es inconsistente")

# ✅ BIEN
def funcion_bien_indentada():
    x = 10
    if x > 5:
        print("esto es correcto")

# Por qué importa:
# - el código se lee de arriba a abajo
# - una indentación clara reduce errores lógicos
# - los linters detectan errores antes de ejecución


# -------------------------------------------------------------------
# 2️⃣ ESPACIOS EN EXPRESIONES
# -------------------------------------------------------------------
#
# El objetivo es LEGIBILIDAD, no ahorrar caracteres.

# ❌ MAL
resultado=precio*1.21+descuento

# ✅ BIEN
resultado = precio * 1.21 + descuento

# Regla mental:
# si el ojo humano tiene que esforzarse, algo está mal.


# -------------------------------------------------------------------
# 3️⃣ LONGITUD DE LÍNEA
# -------------------------------------------------------------------
#
# Regla general:
# - máximo 79 caracteres por línea
# - no es capricho: facilita lectura, diffs y revisiones

# ❌ MAL
resultado_final = calcular_precio_con_descuento_y_impuestos_y_promociones_especiales(precio_base, tipo_usuario, cupon_activo)

# ✅ BIEN
resultado_final = calcular_precio_con_descuento_y_impuestos_y_promociones_especiales(
    precio_base,
    tipo_usuario,
    cupon_activo,
)

# Observa:
# - paréntesis implícitos
# - cada argumento en su línea
# - fácil de modificar sin romper nada


# -------------------------------------------------------------------
# 4️⃣ NOMBRES: VARIABLES
# -------------------------------------------------------------------
#
# Regla:
# - snake_case
# - nombres descriptivos
# - evitar abreviaturas crípticas

# ❌ MAL
x = 10
p = 99.99
d = True

# ✅ BIEN
cantidad_productos = 10
precio_total = 99.99
descuento_activo = True

# El código se lee MUCHAS más veces de las que se escribe.
# Escribe para el lector, no para el teclado.


# -------------------------------------------------------------------
# 5️⃣ NOMBRES: FUNCIONES
# -------------------------------------------------------------------
#
# Regla:
# - verbos + intención
# - que expliquen QUÉ hacen, no CÓMO lo hacen

# ❌ MAL
def calc(p, d):
    return p * d

# ✅ BIEN
def calcular_precio_con_descuento(precio: float, descuento: float) -> float:
    return precio * descuento

# Si el nombre es bueno:
# - no necesitas comentarios
# - no necesitas abrir la función


# -------------------------------------------------------------------
# 6️⃣ NOMBRES: CLASES
# -------------------------------------------------------------------
#
# Regla:
# - PascalCase
# - sustantivos
# - representan conceptos del dominio

# ❌ MAL
class pedido_user:
    pass

# ❌ MAL
class data:
    pass

# ✅ BIEN
class Pedido:
    pass

class Usuario:
    pass


# -------------------------------------------------------------------
# 7️⃣ CONSTANTES
# -------------------------------------------------------------------
#
# Regla:
# - MAYÚSCULAS
# - definidas al inicio del módulo

# ❌ MAL
iva = 1.21

# ✅ BIEN
IVA = 1.21
MAX_INTENTOS_LOGIN = 3

# Las constantes:
# - documentan reglas de negocio
# - evitan "números mágicos"


# -------------------------------------------------------------------
# 8️⃣ ESPACIOS ENTRE FUNCIONES Y CLASES
# -------------------------------------------------------------------
#
# Regla:
# - 2 líneas en blanco entre definiciones de alto nivel
# - 1 línea entre métodos

# ❌ MAL
def a():
    pass
def b():
    pass

# ✅ BIEN
def a():
    pass


def b():
    pass


# -------------------------------------------------------------------
# 9️⃣ IMPORTS (INTRODUCCIÓN, SE PROFUNDIZA DESPUÉS)
# -------------------------------------------------------------------
#
# Orden correcto:
# 1. librería estándar
# 2. librerías externas
# 3. imports locales

# ✅ BIEN
import math
from decimal import Decimal

import numpy as np

from domain.entities.pedido import Pedido


# -------------------------------------------------------------------
# 🔟 POR QUÉ PEP 8 IMPORTA DE VERDAD
# -------------------------------------------------------------------
#
# - Facilita code reviews
# - Reduce discusiones inútiles
# - Permite usar herramientas automáticas (black, flake8, pylint)
# - Hace el código predecible
#
# En equipos:
# el estilo NO se debate, se sigue.
#
# La creatividad está en el diseño,
# no en poner espacios distintos.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# PEP 8 no te hace mejor programador por sí solo,
# pero ignorarlo te hace peor profesional.
#
# Es la base sobre la que se construye:
# - clean code
# - testing
# - arquitectura
# - data pipelines fiables
#
# A partir de aquí, el estilo deja de ser una preocupación.
# Eso libera energía mental para lo importante.
