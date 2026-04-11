"""
mensajes_utiles.py
==================

Objetivo:
- Aprender a escribir mensajes de error claros y descriptivos
- Facilitar debugging y soporte
- Evitar errores crípticos que compliquen mantenimiento
"""

# -------------------------------------------------------------------
# 1️⃣ MENSAJES DE ERROR CLAROS
# -------------------------------------------------------------------

# ❌ Mala práctica: mensaje genérico
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Ocurrió un error")  # ❌ Poco útil

# ✅ Buena práctica: mensaje descriptivo
try:
    x = 10 / 0
except ZeroDivisionError as e:
    print(f"Error al dividir: {e}")  # Output: division by zero

# Ventaja: sabes qué operación falló y por qué

# -------------------------------------------------------------------
# 2️⃣ INCLUIR CONTEXTO EN EL MENSAJE
# -------------------------------------------------------------------

# Ejemplo con función
def procesar_pago(usuario_id: int, monto: float):
    if monto <= 0:
        raise ValueError(f"Monto inválido para el usuario {usuario_id}: {monto}")

try:
    procesar_pago(123, -50)
except ValueError as e:
    print(e)  
    # Output: Monto inválido para el usuario 123: -50

# Contexto ayuda a entender rápidamente el error y cómo reproducirlo

# -------------------------------------------------------------------
# 3️⃣ USAR LOGGING PROFESIONAL
# -------------------------------------------------------------------

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def dividir(a: float, b: float):
    try:
        return a / b
    except ZeroDivisionError as e:
        logging.error(f"Intento de dividir {a} / {b} fallido: {e}")
        return None

resultado = dividir(10, 0)
# Output log: ERROR - Intento de dividir 10 / 0 fallido: division by zero

# Ventaja:
# - Registro persistente
# - Incluye contexto útil
# - Compatible con sistemas profesionales de monitoreo

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PARA MENSAJES DE ERROR
# -------------------------------------------------------------------

# 1. Explicar qué ocurrió, no solo que "falló"
# 2. Incluir contexto relevante (variables, IDs, acciones)
# 3. Evitar información sensible (contraseñas, tokens)
# 4. Usar logging en lugar de print para producción
# 5. Mantener consistencia en formato y nivel de severidad (INFO, WARNING, ERROR, CRITICAL)

# Ejemplo de regla general:
# "Error <tipo> en <función/acción> para <contexto>: <detalle>"
# Esto permite debugging rápido y reproduce problemas con facilidad
