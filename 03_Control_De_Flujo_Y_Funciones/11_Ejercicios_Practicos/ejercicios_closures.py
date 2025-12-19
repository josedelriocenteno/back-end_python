# ejercicios_closures.py
"""
EJERCICIOS DE CLOSURES EN PYTHON
================================

Objetivo:
- Practicar closures: funciones que recuerdan estado
- Aplicación en validadores, configuraciones y factories
- Orientación a backend y pipelines de datos
"""

# =========================================================
# 1. Closure contador
# =========================================================
# Crea un closure que mantenga un contador interno.
# Cada vez que se llame, debe incrementar y devolver el valor actual.
# Ejemplo: contador() -> 1, contador() -> 2, etc.

# =========================================================
# 2. Closure con parámetros iniciales
# =========================================================
# Crea un closure que reciba un multiplicador inicial y devuelva
# otra función que multiplique cualquier número por ese valor.

# =========================================================
# 3. Validador de datos
# =========================================================
# Crea un closure que reciba un tipo de dato permitido (int, str, etc.)
# y devuelva una función que valide si un valor cumple ese tipo,
# devolviendo True/False.

# =========================================================
# 4. Closure como factory
# =========================================================
# Crea un closure que genere funciones para convertir temperaturas:
# - La función principal recibe el tipo de conversión ("CtoF", "FtoC")
# - Devuelve una función que realiza la conversión solicitada

# =========================================================
# 5. Detectar errores comunes
# =========================================================
# - Evita usar variables globales para mantener estado
# - Comprueba que el closure no muta datos externos inesperadamente
# - Asegúrate de que cada closure tenga un único propósito
