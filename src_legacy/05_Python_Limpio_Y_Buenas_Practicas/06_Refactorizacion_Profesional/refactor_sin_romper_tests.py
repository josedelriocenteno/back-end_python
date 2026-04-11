"""
refactor_sin_romper_tests.py
============================

Refactorización segura: cómo cambiar código sin romper tests.

Objetivos:
- Mantener funcionalidad mientras limpias código
- Minimizar riesgos de regresión
- Usar pruebas unitarias y mocks para seguridad
- Aplicar clean code y principios de diseño profesional
"""

# -------------------------------------------------------------------
# 1️⃣ PRINCIPIOS CLAVE
# -------------------------------------------------------------------

# 1. NO refactorices sin tests
# 2. Refactoriza en pequeños pasos
# 3. Ejecuta tests después de cada cambio
# 4. Usa mocks para aislar dependencias externas
# 5. Mantén código antiguo funcionando mientras extraes nueva versión
# 6. Aplica TDD si es posible: test primero, refactor después

# Herramientas recomendadas:
# - pytest: pruebas unitarias
# - unittest.mock: mocks y parches
# - coverage: para asegurarte de cubrir todo el código


# -------------------------------------------------------------------
# 2️⃣ EJEMPLO: FUNCIÓN LEGADA
# -------------------------------------------------------------------

def calcular_total_legado(pedido: dict) -> float:
    """
    Función legada que mezcla validación, cálculo de total y descuentos.
    Necesita refactorización pero debe seguir funcionando igual.
    """
    total = 0
    if pedido.get("productos"):
        for p in pedido["productos"]:
            if p.get("disponible"):
                total += p.get("precio", 0)
    if pedido.get("tipo_usuario") == "premium":
        total *= 0.85
    elif pedido.get("tipo_usuario") == "promo":
        total *= 0.9
    return total


# -------------------------------------------------------------------
# 3️⃣ PASO 1: ESCRIBIR TESTS ANTES DE REFACTORIZAR
# -------------------------------------------------------------------

# tests/test_calcular_total.py
"""
import pytest
from refactor_sin_romper_tests import calcular_total_legado

def test_total_normal():
    pedido = {"productos": [{"precio": 100, "disponible": True}], "tipo_usuario": "normal"}
    assert calcular_total_legado(pedido) == 100

def test_total_premium():
    pedido = {"productos": [{"precio": 100, "disponible": True}], "tipo_usuario": "premium"}
    assert calcular_total_legado(pedido) == 85

def test_total_promo():
    pedido = {"productos": [{"precio": 100, "disponible": True}], "tipo_usuario": "promo"}
    assert calcular_total_legado(pedido) == 90
"""

# ✅ Escribir tests asegura que cualquier cambio posterior no rompa la funcionalidad


# -------------------------------------------------------------------
# 4️⃣ PASO 2: EXTRAER FUNCIONES PEQUEÑAS
# -------------------------------------------------------------------

def calcular_total_productos(productos: list[dict]) -> float:
    """Calcula el total de productos disponibles."""
    return sum(p.get("precio", 0) for p in productos if p.get("disponible", False))

def aplicar_descuento(total: float, tipo_usuario: str) -> float:
    """Aplica descuento según tipo de usuario."""
    if tipo_usuario == "premium":
        return total * 0.85
    elif tipo_usuario == "promo":
        return total * 0.9
    return total


# -------------------------------------------------------------------
# 5️⃣ PASO 3: FUNCIÓN REFACTORIZADA
# -------------------------------------------------------------------

def calcular_total_refactor(pedido: dict) -> float:
    """Refactorización limpia usando funciones pequeñas y SRP."""
    productos = pedido.get("productos", [])
    total = calcular_total_productos(productos)
    total = aplicar_descuento(total, pedido.get("tipo_usuario", "normal"))
    return total


# -------------------------------------------------------------------
# 6️⃣ PASO 4: COMPROBACIÓN CON TESTS
# -------------------------------------------------------------------

# Ejecutar pytest confirma que:
# - Función refactorizada produce mismos resultados que la función legada
# - Puedes cambiar internals sin romper la API externa
# - Riesgo de regresión mínimo


# -------------------------------------------------------------------
# 7️⃣ PASO 5: USO DE MOCKS PARA DEPENDENCIAS EXTERNAS
# -------------------------------------------------------------------

# Ejemplo: si guardar en DB es parte de la función
from unittest.mock import Mock

class RepositorioPedido:
    def guardar(self, pedido: dict):
        print("Guardando en DB...")

def procesar_pedido_con_guardado(pedido: dict, repo: RepositorioPedido):
    total = calcular_total_refactor(pedido)
    repo.guardar({"total": total, "pedido": pedido})
    return total

# Test seguro sin tocar DB
def test_procesar_pedido_con_mock():
    mock_repo = Mock()
    pedido = {"productos": [{"precio": 100, "disponible": True}], "tipo_usuario": "premium"}
    total = procesar_pedido_con_guardado(pedido, mock_repo)
    assert total == 85
    mock_repo.guardar.assert_called_once()  # confirma que se llamó al método
  

# -------------------------------------------------------------------
# 8️⃣ REGLAS DE ORO PARA REFACTORIZAR SIN ROMPER TESTS
# -------------------------------------------------------------------

# 1. Siempre escribir tests antes de refactorizar código legado
# 2. Refactoriza en pasos pequeños, no todo de golpe
# 3. Extrae funciones pequeñas y aplica SRP
# 4. Usa mocks para dependencias externas (DB, APIs, archivos)
# 5. Ejecuta tests después de cada cambio
# 6. Mantén la interfaz externa estable
# 7. Documenta cambios y razones del refactor

# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------

# Refactorización segura = clean code + seguridad
# Con tests y mocks:
# - Puedes limpiar código legada
# - Reducir complejidad
# - Mantener producción estable
# - Prepararte para escalabilidad y mantenimiento profesional
