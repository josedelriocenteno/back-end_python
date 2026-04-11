"""
traceback_analisis.py
=====================

Objetivo:
- Aprender a leer y entender tracebacks en Python
- Identificar rápidamente la causa raíz de errores
- Aplicar estrategias profesionales de debugging
"""

import traceback

# -------------------------------------------------------------------
# 1️⃣ QUÉ ES UN TRACEBACK
# -------------------------------------------------------------------

# Un traceback muestra:
# 1. La secuencia de llamadas (call stack) hasta el error
# 2. La línea exacta donde ocurrió
# 3. Tipo de excepción y mensaje

def dividir(a, b):
    return a / b

def procesar_valores(x, y):
    return dividir(x, y)

# Este código generará un ZeroDivisionError
try:
    procesar_valores(10, 0)
except Exception as e:
    print("❌ Ocurrió un error:", e)
    # Mostrar traceback completo
    traceback.print_exc()

# Output ejemplo:
# Traceback (most recent call last):
#   File "traceback_analisis.py", line 21, in <module>
#     procesar_valores(10, 0)
#   File "traceback_analisis.py", line 18, in procesar_valores
#     return dividir(x, y)
#   File "traceback_analisis.py", line 15, in dividir
#     return a / b
# ZeroDivisionError: division by zero

# -------------------------------------------------------------------
# 2️⃣ CÓMO INTERPRETAR TRACEBACKS
# -------------------------------------------------------------------

# 1️⃣ Revisar la última línea: indica el tipo de excepción y mensaje
#    → ZeroDivisionError: division by zero

# 2️⃣ Revisar call stack (líneas anteriores):
#    → Muestra la secuencia de funciones que llevaron al error
#    → Permite identificar dónde en tu código ocurrió la llamada problemática

# 3️⃣ Revisar archivos y números de línea
#    → Facilita saltar directo a la línea de código que causó el fallo

# -------------------------------------------------------------------
# 3️⃣ USO PROFESIONAL
# -------------------------------------------------------------------

def safe_dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        # Loggear con contexto completo
        import logging
        logging.error(f"Error al dividir {a} / {b}", exc_info=True)
        return None

resultado = safe_dividir(10, 0)
print("Resultado seguro:", resultado)

# - exc_info=True agrega traceback completo al log
# - Permite debug profesional sin romper la aplicación
# - Complementa logging configurado y manejo de errores

# -------------------------------------------------------------------
# 4️⃣ CONSEJOS PROFESIONALES
# -------------------------------------------------------------------

# 1. Siempre leer de abajo hacia arriba: la última línea indica el error real
# 2. Ignorar llamadas a librerías externas inicialmente; concentrarse en tu código
# 3. Usar logging con exc_info para capturar tracebacks en producción
# 4. Combinar con try/except y fail-fast para errores críticos
# 5. Evitar print de traceback en producción, usar logs persistentes

# -------------------------------------------------------------------
# 5️⃣ EXTRA: OBTENER TRACEBACK COMO STRING
# -------------------------------------------------------------------

try:
    procesar_valores(5, 0)
except Exception:
    tb_str = traceback.format_exc()
    # Podemos enviar a logs, sistemas de monitoreo, alertas
    print("TRACEBACK COMO STRING:\n", tb_str)

# Esto es útil para depuración remota o envío de errores a un sistema externo
