# ejercicios_decorators.py
"""
EJERCICIOS DE DECORATORS EN PYTHON
==================================

Objetivo:
- Practicar decorators básicos y avanzados
- Comprender functools.wraps, decorators con parámetros y uso en backend
- Aplicación a logging, caching, auth y timing
"""

# =========================================================
# 1. Decorator simple
# =========================================================
# Crea un decorator que imprima "Inicio función" antes de ejecutar
# y "Fin función" después de ejecutar cualquier función pasada.

# =========================================================
# 2. Decorator con retorno
# =========================================================
# Modifica el decorator anterior para que también imprima
# el valor de retorno de la función decorada.

# =========================================================
# 3. Decorator con parámetros
# =========================================================
# Crea un decorator que reciba un mensaje como parámetro
# y lo imprima antes de ejecutar la función.

# =========================================================
# 4. Decorator de tiempo
# =========================================================
# Crea un decorator que calcule el tiempo de ejecución
# de la función decorada y lo imprima en consola.

# =========================================================
# 5. Decorator para autenticación
# =========================================================
# Simula un decorator que compruebe un token ficticio antes
# de ejecutar la función. Si no es válido, lanza excepción.

# =========================================================
# 6. functools.wraps
# =========================================================
# Redefine cualquier decorator anterior usando functools.wraps
# y comprueba que el __name__ y __doc__ de la función decorada
# se mantienen intactos.

# =========================================================
# 7. Errores comunes
# =========================================================
# - No olvidar retornar la función interna
# - No mutar parámetros de entrada de forma inesperada
# - Evitar efectos secundarios innecesarios
