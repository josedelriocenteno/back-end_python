# ejercicios_mixtos.py
"""
EJERCICIOS MIXTOS DE CONTROL DE FLUJO Y FUNCIONES
================================================

Objetivo:
- Integrar condicionales, bucles, funciones, closures y decorators
- Resolver problemas típicos de backend y pipelines de datos
- Aplicar buenas prácticas, tipado, docstrings y control de errores
"""

# =========================================================
# 1. Pipeline de validación
# =========================================================
# Crea una función que reciba una lista de diccionarios con usuarios.
# Valida que cada usuario tenga 'nombre' y 'edad' > 0.
# Devuelve solo los válidos.
# Usa funciones auxiliares, condicionales y bucles.

# =========================================================
# 2. Contador con closure
# =========================================================
# Implementa un closure que cuente cuántos usuarios cumplen
# cierto criterio (por ejemplo, mayores de 18 años).
# Integra este closure dentro de tu pipeline anterior.

# =========================================================
# 3. Decorator de logging
# =========================================================
# Crea un decorator que imprima al inicio y final de cada función
# del pipeline: nombre de función y número de registros procesados.

# =========================================================
# 4. Transformación de datos
# =========================================================
# Crea una función que transforme los nombres de los usuarios
# a minúsculas y elimine espacios al inicio y fin.
# Aplica esta función a toda la lista usando un bucle o comprehension.

# =========================================================
# 5. Estadísticas simples
# =========================================================
# Crea una función que calcule:
# - Número total de usuarios
# - Número de usuarios mayores de 18
# - Promedio de edad
# Devuelve los resultados en un diccionario.

# =========================================================
# 6. Errores controlados
# =========================================================
# Modifica tu pipeline para capturar errores:
# - Usuarios con edades no numéricas
# - Nombres vacíos
# Usa try/except y registra los errores sin detener la ejecución.

# =========================================================
# 7. Integración final
# =========================================================
# Combina todo en un solo pipeline profesional:
# - Validación
# - Transformación
# - Estadísticas
# - Logging
# - Contadores con closure
# Asegúrate de que las funciones sean puras siempre que sea posible.
