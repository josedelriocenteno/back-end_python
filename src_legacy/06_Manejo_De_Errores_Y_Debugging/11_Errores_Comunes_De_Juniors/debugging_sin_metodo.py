"""
debugging_sin_metodo.py
========================

Objetivo:
- Mostrar los problemas de depuración sin método
- Enseñar un enfoque organizado y profesional de debugging
"""

import logging

# -------------------------------------------------------------------
# 1️⃣ ANTI-PATRÓN: debugging desordenado
# -------------------------------------------------------------------

def funcion_caotica():
    x = 10
    y = 0
    z = None
    # Debugging improvisado
    print("Valor de x:", x)
    print("Valor de y:", y)
    print("Intentando dividir...")
    resultado = x / y  # ❌ Genera ZeroDivisionError sin control
    print("Resultado:", resultado)
    z = x + y
    print("Valor de z:", z)

# Problemas:
# - Uso indiscriminado de print → logs mezclados con outputs
# - Errores inesperados sin manejo → crash del programa
# - Difícil reproducir pasos exactos
# - No hay trazabilidad ni contexto de variables críticas

# -------------------------------------------------------------------
# 2️⃣ FORMA PROFESIONAL: debugging estructurado
# -------------------------------------------------------------------

def funcion_debuggable():
    logging.info("Inicio de la función debuggable")
    x = 10
    y = 0

    try:
        resultado = x / y
    except ZeroDivisionError as e:
        logging.error(f"Error de división por cero: x={x}, y={y}", exc_info=True)
        resultado = None  # Valor de fallback
    finally:
        z = x + y
        logging.info(f"Valor de z calculado correctamente: {z}")

    logging.info(f"Resultado final de la operación: {resultado}")
    return resultado, z

# -------------------------------------------------------------------
# 3️⃣ EJECUCIÓN
# -------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("Ejecutando función caótica (anti-patrón)...")
    try:
        funcion_caotica()
    except Exception as e:
        print("Crash inesperado:", e)

    print("\nEjecutando función debuggable (profesional)...")
    funcion_debuggable()

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES DE DEBUGGING
# -------------------------------------------------------------------

# 1️⃣ Evitar prints dispersos → usar logging con niveles
# 2️⃣ Capturar excepciones esperadas y loggear contexto
# 3️⃣ Mantener trazabilidad de variables críticas
# 4️⃣ Usar bloques try/except/finally claros
# 5️⃣ Separar debugging de lógica de negocio
# 6️⃣ Documentar pasos de debugging y valores de prueba
# 7️⃣ Usar asserts y tests unitarios para verificar invariantes
# 8️⃣ Mantener consistencia entre entornos desarrollo y producción
