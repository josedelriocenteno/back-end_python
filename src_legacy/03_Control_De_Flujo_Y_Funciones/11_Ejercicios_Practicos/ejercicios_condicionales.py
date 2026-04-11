# ejercicios_condicionales.py
"""
EJERCICIOS DE CONDICIONALES EN PYTHON
=====================================

Objetivo:
- Practicar if/elif/else, operadores lógicos y guard clauses
- Detectar errores comunes y escribir condicionales claras y legibles
- Orientación a backend y pipelines de datos
"""

# =========================================================
# 1. Edad y permisos
# =========================================================
# Escribe una función que reciba la edad de una persona
# y devuelva:
# - "Menor de edad" si es < 18
# - "Adulto" si es entre 18 y 64
# - "Senior" si es >= 65
# Debe usar condicionales legibles y sin anidar if innecesariamente.

# =========================================================
# 2. Validación de datos de usuario
# =========================================================
# Escribe una función que reciba un diccionario con campos:
# 'nombre', 'email', 'edad'
# Debe devolver True si todos los campos son válidos:
# - nombre no vacío
# - email contiene '@'
# - edad >= 0
# Usa guard clauses para evitar if anidados.

# =========================================================
# 3. Categoría de productos
# =========================================================
# Dado un diccionario de producto con 'precio' y 'categoria',
# escribe una función que clasifique los productos así:
# - Si es 'alimentación' y precio < 5 -> "Económico"
# - Si es 'alimentación' y precio >= 5 -> "Normal"
# - Si es 'tecnología' -> "Premium"
# - Otros -> "Genérico"

# =========================================================
# 4. Validación múltiple con operadores lógicos
# =========================================================
# Escribe una función que reciba un usuario con campos:
# 'edad', 'pais', 'activo'
# Debe devolver True solo si:
# - Edad >= 18
# - Pais es "España" o "Portugal"
# - Activo es True

# =========================================================
# 5. Detectar errores comunes
# =========================================================
# Reescribe los siguientes condicionales para que sean más claros:
# - if edad >= 18 and edad <= 65:
# - if not (activo == False):
# - if pais == "España" or pais == "Portugal" or pais == "Andorra":
# Identifica redundancias y simplifícalos usando buenas prácticas
