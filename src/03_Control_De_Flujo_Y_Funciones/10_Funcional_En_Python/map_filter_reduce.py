# map_filter_reduce.py
"""
USO DE MAP, FILTER Y REDUCE EN PYTHON
=====================================

Objetivo:
- Aplicar map, filter y reduce en contextos reales de backend y data pipelines
- Mantener código limpio, eficiente y fácil de testear
- Evitar mal uso académico que no aporta en producción
"""

from functools import reduce
from typing import List, Dict, Any

# =========================================================
# 1. map: transformación de datos
# =========================================================
def extraer_emails(registros: List[Dict[str, Any]]) -> List[str]:
    """
    Extrae la lista de emails de los registros.

    Args:
        registros: lista de diccionarios con campo 'email'

    Returns:
        lista de emails
    """
    return list(map(lambda r: r.get("email", "").lower(), registros))

# Ejemplo real
usuarios = [{"email": "ANA@EMAIL.COM"}, {"email": "Luis@correo.com"}]
emails = extraer_emails(usuarios)
print(emails)  # ['ana@email.com', 'luis@correo.com']

# =========================================================
# 2. filter: filtrado de datos
# =========================================================
def filtrar_mayores_edad(registros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filtra los registros donde 'edad' >= 18
    """
    return list(filter(lambda r: r.get("edad", 0) >= 18, registros))

# =========================================================
# 3. reduce: agregación de datos
# =========================================================
def sumar_montos(ventas: List[Dict[str, Any]]) -> float:
    """
    Suma los montos de una lista de ventas usando reduce
    """
    return reduce(lambda acc, v: acc + float(v.get("monto", 0)), ventas, 0.0)

# Ejemplo real
ventas = [{"monto": 100}, {"monto": 250}, {"monto": 50}]
total = sumar_montos(ventas)
print(total)  # 400.0

# =========================================================
# 4. Combinación: pipeline simple
# =========================================================
def pipeline_filtrar_y_sumar(registros: List[Dict[str, Any]]) -> float:
    """
    Filtra mayores de edad y suma un campo 'monto'
    """
    mayores = filter(lambda r: r.get("edad", 0) >= 18, registros)
    total = reduce(lambda acc, r: acc + r.get("monto", 0), mayores, 0)
    return total

# =========================================================
# 5. Buenas prácticas
# =========================================================
# - Evitar funciones lambda muy largas o complejas
# - Usar map/filter/reduce solo cuando mejora legibilidad
# - Mantener pipelines claros y composables
# - Documentar inputs y outputs
# - Preparar para batch y streaming en pipelines de datos
# - Testear cada función de forma aislada
