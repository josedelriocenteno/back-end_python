# ejercicios_funciones.py
"""
EJERCICIOS DE FUNCIONES EN PYTHON
=================================

Objetivo:
- Practicar definición de funciones, argumentos, retorno, funciones puras
- Usar *args, **kwargs, tipado, docstrings
- Orientación a backend, pipelines de datos y testing
"""

# =========================================================
# 1. Función básica
# =========================================================
# Crea una función que reciba una lista de números y devuelva
# la suma de los positivos únicamente. Debe ser pura, sin mutar la lista.

# =========================================================
# 2. Parámetros y valores por defecto
# =========================================================
# Crea una función que reciba nombre y rol de un usuario.
# Si no se proporciona el rol, debe asumir 'invitado'.
# Devuelve un diccionario con la información.

# =========================================================
# 3. *args y **kwargs
# =========================================================
# Crea una función que reciba cualquier cantidad de números
# (*args) y devuelva su promedio.
# Luego, extiende la función para recibir un diccionario de opciones (**kwargs)
# que pueda incluir 'redondeo' para definir los decimales del promedio.

# =========================================================
# 4. Funciones puras y composición
# =========================================================
# Crea dos funciones puras:
# - Una que filtre usuarios mayores de 18
# - Otra que normalice los nombres a minúsculas
# Combínalas en un pipeline que reciba una lista de usuarios
# y devuelva la lista transformada, sin mutar los datos originales.

# =========================================================
# 5. Docstrings y tipado
# =========================================================
# Redefine cualquier función anterior añadiendo:
# - Tipado completo de parámetros y retorno
# - Docstrings explicativos con ejemplo de uso

# =========================================================
# 6. Detectar errores comunes
# =========================================================
# Analiza y corrige las siguientes funciones para que sean puras:
# - Evita mutar listas o diccionarios de entrada
# - Asegúrate de que cada función tenga un único propósito
# - Simplifica condicionales dentro de la función
