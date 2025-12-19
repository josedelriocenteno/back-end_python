# lambda_functions.py
"""
FUNCIONES LAMBDA EN PYTHON
==========================

Objetivo:
- Entender cuándo usar funciones lambda y cuándo evitarlas
- Mantener código limpio, legible y eficiente
- Aplicarlas correctamente en pipelines, map/filter y callbacks
"""

from typing import List, Dict

# =========================================================
# 1. Qué es una lambda
# =========================================================
# Una lambda es una función anónima, inline, que se define en una sola línea.
# Sintaxis:
#   lambda argumentos: expresión

# Ejemplo simple
suma = lambda x, y: x + y
print(suma(3, 4))  # 7

# =========================================================
# 2. Uso real en backend / data pipelines
# =========================================================
# Ejemplo: extraer campos de un diccionario
usuarios = [{"nombre": "Ana", "edad": 25}, {"nombre": "Luis", "edad": 17}]

nombres = list(map(lambda u: u["nombre"].upper(), usuarios))
print(nombres)  # ['ANA', 'LUIS']

# Filtrar mayores de edad
mayores = list(filter(lambda u: u["edad"] >= 18, usuarios))
print(mayores)  # [{'nombre': 'Ana', 'edad': 25}]

# =========================================================
# 3. Cuándo usar lambdas
# =========================================================
# ✅ Funciones pequeñas, temporales y claras
# ✅ Callbacks en APIs, map/filter/reduce
# ✅ Transformaciones inline que no se reutilizan

# =========================================================
# 4. Cuándo NO usar lambdas
# ❌ Funciones complejas con varias líneas o lógica condicional
# ❌ Funciones que se reutilizan: mejor definir con def
# ❌ Si afecta la legibilidad o comprensión del código

# Ejemplo de mal uso
# lista_ordenada = sorted(usuarios, key=lambda u: u["edad"] if u["edad"] > 18 else 0)
# Mejor escribir una función separada para claridad

# =========================================================
# 5. Buenas prácticas profesionales
# =========================================================
# - Mantener lambdas legibles y cortas
# - Evitar side-effects dentro de lambdas
# - Preferir def para funciones complejas o reutilizables
# - Documentar cuando se usa en pipelines de datos
# - Combinarlas con map/filter/reduce solo si mejora claridad
