"""
resumen_python_limpio.py
========================

Resumen completo: Python limpio y buenas prácticas

Incluye:
- Estilo y convenciones (PEP8)
- Tipado estático y Protocols
- Docstrings y documentación
- Manejo de complejidad y SRP
- Linters y formateadores
- Refactorización profesional
- Errores comunes de juniors
- Buenas prácticas en backend
- Buenas prácticas en Data/ML
"""

# -------------------------------------------------------------------
# 1️⃣ ESTILO Y CONVENCIONES
# -------------------------------------------------------------------

# Nombres claros
nombre_variable = 10           # ✅ descriptivo
nombre_funcion()               # ✅ verbo para función
class NombreClase:             # ✅ PascalCase
    pass

# Espacios y líneas
x = 1
y = 2  # espacios correctos
if x == y:  # indentación correcta
    print(x + y)

# Imports
import os
import sys

# -------------------------------------------------------------------
# 2️⃣ TIPADO ESTÁTICO
# -------------------------------------------------------------------

from typing import List, Optional, Union, Protocol
from dataclasses import dataclass

def suma(a: int, b: int) -> int:
    return a + b

@dataclass
class Usuario:
    id: str
    nombre: str
    email: str

# Protocols
class DescuentoStrategy(Protocol):
    def aplicar(self, subtotal: float) -> float:
        ...

# -------------------------------------------------------------------
# 3️⃣ DOCSTRINGS Y DOCUMENTACIÓN
# -------------------------------------------------------------------

def funcion_ejemplo(x: int, y: int) -> int:
    """
    Suma dos enteros y devuelve el resultado.
    
    Args:
        x (int): Primer número
        y (int): Segundo número
        
    Returns:
        int: Suma de x + y
    """
    return x + y

# -------------------------------------------------------------------
# 4️⃣ MANEJO DE COMPLEJIDAD
# -------------------------------------------------------------------

# Funciones pequeñas
def calcular_total(productos: List[dict]) -> float:
    """Calcula total de lista de productos"""
    return sum(p["precio"] for p in productos)

# Guard clauses en lugar de if anidados
def procesar_usuario(usuario: Optional[Usuario]):
    if usuario is None:
        return
    print(usuario.nombre)

# Separar responsabilidades
def procesar_pedido(pedido):
    calcular_total(pedido["productos"])
    enviar_notificacion(pedido["usuario"])

# -------------------------------------------------------------------
# 5️⃣ LINTEOS Y FORMATOS
# -------------------------------------------------------------------

# Ejecutar flake8, pylint y black regularmente
# isort para organizar imports
# Configuración en pyproject.toml para consistencia

# -------------------------------------------------------------------
# 6️⃣ REFACTORIZACIÓN PROFESIONAL
# -------------------------------------------------------------------

# Identificar code smells
# Funciones largas → dividir
# Clases grandes → SRP y composición
# Tests antes y después de refactorizar

# -------------------------------------------------------------------
# 7️⃣ ERRORES COMUNES DE JUNIORS
# -------------------------------------------------------------------

# Funciones gigantes
def funcion_gigante():
    pass  # ❌ anti-pattern

# Clases dios
class ClaseDios:
    pass  # ❌ anti-pattern

# Sobreingeniería
def abstraccion_innecesaria():
    pass  # ❌ anti-pattern

# -------------------------------------------------------------------
# 8️⃣ BUENAS PRÁCTICAS EN BACKEND
# -------------------------------------------------------------------

# Separación de capas: API / dominio / infraestructura
# Configuración externa (settings, env vars)
# Logging consistente
# Manejo centralizado de errores
# Dependencias inyectadas explícitamente

# -------------------------------------------------------------------
# 9️⃣ BUENAS PRÁCTICAS EN DATA/ML
# -------------------------------------------------------------------

import pandas as pd
import numpy as np

# Funciones puras
def agregar_feature(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["x2"] = df["x"] ** 2
    return df

# Fijar seeds
SEED = 42
np.random.seed(SEED)

# Versionado de datos y modelos
# dataset_v1.csv, modelo_v1.pkl
# Metadata y hashes para reproducibilidad

# Pipelines reproducibles
def pipeline(df: pd.DataFrame):
    df = agregar_feature(df)
    # Guardar salida y reportar aparte para evitar side effects
    return df

# -------------------------------------------------------------------
# 10️⃣ CHECKLISTS Y ESTÁNDARES
# -------------------------------------------------------------------

# Antes de entregar código
checklist_codigo_profesional = [
    "PEP8 y estilo",
    "Nombres claros",
    "Docstrings completos",
    "Tests unitarios",
    "Tipado completo",
    "Funciones puras",
    "Side effects controlados",
]

# Proyecto backend listo para producción
checklist_backend = [
    "Separación de capas",
    "Inyección de dependencias",
    "Logging y manejo de errores",
    "Configuración externa",
    "Tests y reproducibilidad",
]

# Code review
checklist_code_review = [
    "Legibilidad y estilo",
    "Complejidad y modularidad",
    "Tipado y validaciones",
    "Seguridad y manejo de secretos",
    "Tests y reproducibilidad",
    "Documentación y comentarios",
]

# -------------------------------------------------------------------
# 11️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Este archivo resume los principios clave de:
# - Python limpio y mantenible
# - Buenas prácticas en backend y Data/ML
# - Checklist de entrega, revisión y producción
#
# Sirve como referencia rápida para proyectos reales y refactorizaciones.
