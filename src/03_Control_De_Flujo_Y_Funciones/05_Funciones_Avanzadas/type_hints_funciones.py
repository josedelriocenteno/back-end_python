# type_hints_funciones.py
"""
TIPADO PROFESIONAL EN FUNCIONES PYTHON
=====================================

Objetivo:
- Aplicar type hints para mejorar claridad, seguridad y mantenibilidad
- Facilitar debugging, testing y colaboración en proyectos backend
- Preparar código para linters, herramientas de análisis estático y IDEs profesionales

Contexto:
- Python es dinámico, pero el tipado ayuda a documentar y prevenir errores
- Usar type hints no cambia el comportamiento, solo añade información
- Muy útil en APIs, pipelines y funciones complejas con muchos parámetros
"""

from typing import List, Dict, Tuple, Union, Optional

# =========================================================
# 1. Tipado básico
# =========================================================

def sumar(a: int, b: int) -> int:
    """
    Suma dos enteros
    """
    return a + b

resultado: int = sumar(5, 10)
print(resultado)

# =========================================================
# 2. Tipos comunes en backend/data pipelines
# =========================================================

# Listas y diccionarios
def procesar_datos(datos: List[int]) -> List[int]:
    """
    Duplica cada valor de la lista
    """
    return [x*2 for x in datos]

def contar_frecuencia(items: List[str]) -> Dict[str, int]:
    """
    Devuelve un diccionario con la frecuencia de cada string
    """
    resultado: Dict[str, int] = {}
    for item in items:
        resultado[item] = resultado.get(item, 0) + 1
    return resultado

# Tuplas y Unions
def dividir_y_restar(a: float, b: float) -> Tuple[float, float]:
    """
    Devuelve (a/b, a-b)
    """
    return (a/b, a-b)

def parse_valor(valor: Union[int, str]) -> int:
    """
    Convierte valor a int si es str
    """
    if isinstance(valor, int):
        return valor
    return int(valor)

# =========================================================
# 3. Tipos opcionales y predeterminados
# =========================================================

def buscar_usuario(id_usuario: int, tabla: Optional[List[Dict]] = None) -> Dict:
    """
    Busca un usuario en la tabla, tabla opcional
    """
    if tabla is None:
        tabla = []
    for user in tabla:
        if user.get("id") == id_usuario:
            return user
    return {}

# =========================================================
# 4. Funciones más complejas con tipado
# =========================================================

from typing import Callable

def aplicar_transformacion(
    datos: List[int], transform: Callable[[int], int]
) -> List[int]:
    """
    Aplica una función a cada elemento de la lista
    """
    return [transform(x) for x in datos]

# Ejemplo
print(aplicar_transformacion([1,2,3], lambda x: x**2))  # [1,4,9]

# =========================================================
# 5. Buenas prácticas en backend y pipelines
# =========================================================

# - Siempre tipar parámetros y retorno, especialmente en funciones públicas
# - Usar Optional para valores que pueden ser None
# - Usar Union para inputs que aceptan múltiples tipos
# - Documentar con docstrings y type hints juntos
# - Combinar con linters como mypy para análisis estático
# - Facilita mantenimiento, colaboración y detección temprana de errores
