# funciones_para_pipelines.py
"""
FUNCIONES PARA PIPELINES DE DATOS
=================================

Objetivo:
- Crear funciones claras, pequeñas y reutilizables para pipelines de datos
- Mantener transformaciones puras, testables y seguras
- Evitar efectos secundarios inesperados en procesamiento batch o streaming
"""

from typing import List, Dict, Any

# =========================================================
# 1. Función pura: transformación de datos
# =========================================================
def normalizar_nombres(registros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normaliza el campo 'nombre' de cada registro: trim, lowercase.

    Args:
        registros (list of dict): Datos a procesar

    Returns:
        list of dict: Datos normalizados
    """
    resultado = []
    for r in registros:
        nuevo = r.copy()  # evitar mutar original
        nombre = nuevo.get("nombre", "")
        nuevo["nombre"] = nombre.strip().lower()
        resultado.append(nuevo)
    return resultado

# =========================================================
# 2. Función con validación de datos
# =========================================================
def filtrar_registros_validos(registros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filtra registros que cumplan ciertas reglas de negocio.
    Ej: deben tener 'email' válido y 'edad' positiva.
    """
    filtrados = [
        r for r in registros
        if "email" in r and "@" in r["email"]
        and isinstance(r.get("edad", 0), int) and r["edad"] > 0
    ]
    return filtrados

# =========================================================
# 3. Composición de funciones: pipelines limpios
# =========================================================
def procesar_pipeline(registros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Pipeline completo: filtra y normaliza.
    """
    return normalizar_nombres(filtrar_registros_validos(registros))

# =========================================================
# 4. Funciones para agregaciones
# =========================================================
def sumar_ventas_por_categoria(ventas: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Agrega ventas por categoría.

    Args:
        ventas (list of dict): Cada venta con 'categoria' y 'monto'

    Returns:
        dict: Total por categoría
    """
    totales = {}
    for venta in ventas:
        cat = venta.get("categoria", "otros")
        monto = float(venta.get("monto", 0))
        totales[cat] = totales.get(cat, 0) + monto
    return totales

# =========================================================
# 5. Buenas prácticas profesionales
# =========================================================
# - Mantener funciones puras siempre que sea posible
# - No mutar listas/dicts de entrada
# - Documentar claramente inputs/outputs
# - Componer funciones pequeñas para crear pipelines complejos
# - Testear funciones individualmente y en pipeline completo
# - Preparar funciones para batch y streaming, evitando efectos secundarios
# - Usar type hints para claridad y autocompletado en IDEs
