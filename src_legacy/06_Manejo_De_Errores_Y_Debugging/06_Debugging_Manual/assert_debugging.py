"""
assert_debugging.py
==================

Objetivo:
- Usar `assert` para validar condiciones esperadas en desarrollo
- Detectar errores lógicos temprano (fail-fast)
- Mantener código limpio y profesional
"""

# -------------------------------------------------------------------
# 1️⃣ QUÉ ES assert
# -------------------------------------------------------------------

# assert permite verificar que una condición sea True
# Si es False, lanza AssertionError con un mensaje opcional

x = 10
y = 5

assert x > y, f"ERROR: x ({x}) debería ser mayor que y ({y})"

# Si x <= y, el programa se detiene inmediatamente con un mensaje claro

# -------------------------------------------------------------------
# 2️⃣ USO PARA DEBUGGING
# -------------------------------------------------------------------

# Ejemplo: verificar valores de entrada de funciones

def calcular_promedio(lista):
    # Fail-fast si lista vacía
    assert isinstance(lista, list), "ERROR: lista debe ser tipo list"
    assert len(lista) > 0, "ERROR: lista no puede estar vacía"
    return sum(lista) / len(lista)

promedio = calcular_promedio([10, 20, 30])
print("Promedio:", promedio)

# -------------------------------------------------------------------
# 3️⃣ BENEFICIOS PROFESIONALES
# -------------------------------------------------------------------

# 1. Detecta errores lógicos temprano
# 2. Facilita debugging sin saturar la consola
# 3. Complementa logging: assert falla rápido, logging registra información
# 4. Ideal para invariantes de funciones y clases
# 5. No reemplaza manejo de excepciones en producción

# -------------------------------------------------------------------
# 4️⃣ CUANDO NO USAR assert
# -------------------------------------------------------------------

# ❌ No usar assert para manejo de errores de usuario
# assert edad > 0, "Edad inválida"  # ❌ Mal, esto debe ser ValueError
# ❌ No usar assert para flujos de negocio en producción
# assert pago > 0, "Pago inválido"  # ❌ Mejor lanzar excepción controlada

# -------------------------------------------------------------------
# 5️⃣ USO PROFESIONAL CON FLAGS DE DEBUG
# -------------------------------------------------------------------

DEBUG = True

def procesar_registro(registro):
    if DEBUG:
        assert "id" in registro, "Registro sin ID"
        assert "valor" in registro, "Registro sin valor"
    # Lógica normal
    return registro["valor"] * 2

procesar_registro({"id": 1, "valor": 10})

# -------------------------------------------------------------------
# 6️⃣ RESUMEN
# -------------------------------------------------------------------

# - assert: herramienta para fail-fast en desarrollo
# - Siempre incluir mensaje claro para debug
# - Usar solo para condiciones internas, invariantes y desarrollo
# - Para errores de usuario o producción → lanzar excepciones apropiadas
# - Complementa logging y testing, no lo reemplaza
