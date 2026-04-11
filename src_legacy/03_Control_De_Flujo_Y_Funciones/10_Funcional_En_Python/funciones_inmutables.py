# funciones_inmutables.py
"""
FUNCIONES INMUTABLES EN PYTHON
===============================

Objetivo:
- Aplicar estilo funcional en pipelines y backend
- Evitar efectos secundarios y mutaciones inesperadas
- Garantizar que las funciones sean puras y testables
- Mejorar mantenibilidad y claridad en procesamiento de datos
"""

from typing import List, Dict, Any
from copy import deepcopy

# =========================================================
# 1. Qué significa inmutable
# =========================================================
# Inmutable: la función no cambia los datos de entrada, sino que devuelve nuevos datos.
# Beneficios:
# - Evita bugs silenciosos por mutaciones
# - Facilita testing unitario
# - Compatible con programación funcional y pipelines

# =========================================================
# 2. Ejemplo simple
# =========================================================
def incrementar_edades(registros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Incrementa la edad de cada registro +1, sin mutar la lista original
    """
    return [{**r, "edad": r.get("edad", 0) + 1} for r in registros]

usuarios = [{"nombre": "Ana", "edad": 25}, {"nombre": "Luis", "edad": 17}]
nuevos = incrementar_edades(usuarios)

print(usuarios)  # original intacto
print(nuevos)    # [{'nombre': 'Ana', 'edad': 26}, {'nombre': 'Luis', 'edad': 18}]

# =========================================================
# 3. Uso de deepcopy para objetos anidados
# =========================================================
def actualizar_contacto(registros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Actualiza teléfonos, evitando modificar registros originales (deep copy)
    """
    registros_nuevos = deepcopy(registros)
    for r in registros_nuevos:
        r["telefono"] = r.get("telefono", "000-000") + "-X"
    return registros_nuevos

# =========================================================
# 4. Composición de funciones puras (pipeline)
# =========================================================
def pipeline_inmutable(registros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Pipeline de transformación inmutable:
    1. Filtra mayores de edad
    2. Incrementa edad
    3. Normaliza nombres
    """
    def filtrar_mayores(r):
        return r.get("edad", 0) >= 18

    def normalizar_nombre(r):
        return {**r, "nombre": r.get("nombre", "").strip().lower()}

    # Composición funcional
    return [normalizar_nombre(r) for r in registros if filtrar_mayores(r)]

# =========================================================
# 5. Buenas prácticas profesionales
# =========================================================
# - Mantener funciones puras: mismas entradas → mismas salidas
# - No mutar listas o diccionarios de entrada
# - Evitar side effects: logging, prints o IO dentro de la función
# - Usar comprehensions y copy/deepcopy según necesidad
# - Facilita testing unitario y reproducibilidad de pipelines
# - Encadenar funciones puras para crear pipelines claros y mantenibles
