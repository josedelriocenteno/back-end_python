"""
no_ocultar_errores.py
=====================

Objetivo:
- Identificar el anti-pattern de ocultar errores
- Comprender riesgos de capturar excepciones sin manejarlas
- Aprender buenas prácticas para debug y mantenimiento
"""

# -------------------------------------------------------------------
# 1️⃣ ANTI-PATTERN: OCULTAR ERRORES
# -------------------------------------------------------------------

# ❌ Mala práctica: except vacío o solo pass
try:
    x = 10 / 0
except:
    pass  # Error completamente ignorado ⚠️

# Problemas:
# 1. Difícil de debuggear: no sabes qué fallo
# 2. Puede generar datos inconsistentes
# 3. Rompe fail-fast principle
# 4. Oculta bugs de lógica, no solo errores esperados

# -------------------------------------------------------------------
# 2️⃣ MEJOR PRÁCTICA: CAPTURA Y LOGGING
# -------------------------------------------------------------------

import logging

logging.basicConfig(level=logging.INFO)

try:
    x = 10 / 0
except ZeroDivisionError as e:
    logging.error(f"Se capturó error: {e}")
    # Decidir acción correctiva
    x = 0

print(f"x = {x}")  # Output: x = 0, error registrado

# -------------------------------------------------------------------
# 3️⃣ OCULTAR ERRORES SOLO CUANDO ES SEGURO
# -------------------------------------------------------------------

# Ejemplo: error esperado y recuperable
def leer_config(path: str):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Si falta config, usar valor por defecto ✅
        logging.warning(f"No se encontró {path}, usando defaults")
        return "{}"

config = leer_config("config_inexistente.json")
print(config)  # Output: {}

# Nota: aquí el error no se "oculta", sino que se maneja con lógica segura

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# 1. Nunca uses except vacío o genérico sin justificación
# 2. Siempre que captures errores, decide:
#    - Loguearlo
#    - Re-lanzarlo si es crítico
#    - Corregir o degradar funcionalidad si es seguro
# 3. Captura solo excepciones esperadas
# 4. Mantén el flujo principal limpio y legible
# 5. Evita ocultar errores de lógica o programación
