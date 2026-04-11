"""
silencios_peligrosos.py
=========================

Objetivo:
- Mostrar por qué ignorar excepciones es extremadamente peligroso
- Enseñar cómo manejar errores correctamente para debugging y producción
"""

import logging

# -------------------------------------------------------------------
# 1️⃣ ANTI-PATRÓN: capturar y no hacer nada
# -------------------------------------------------------------------

def division_riesgosa(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        # ❌ Anti-patrón: se ignora el error
        pass

resultado = division_riesgosa(10, 0)
print("Resultado ignorando error:", resultado)  # None, pero sin contexto

# Problemas:
# - El error desaparece sin dejar rastro
# - Debugging imposible
# - Puede causar efectos secundarios silenciosos

# -------------------------------------------------------------------
# 2️⃣ FORMA PROFESIONAL: loggear y/o manejar
# -------------------------------------------------------------------

def division_segura(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        logging.warning(f"Intento de división por cero: {a} / {b}")
        return float('inf')  # O valor de fallback razonable

resultado_seguro = division_segura(10, 0)
print("Resultado seguro:", resultado_seguro)

# -------------------------------------------------------------------
# 3️⃣ RECOMENDACIONES PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Nunca ignorar excepciones sin contexto
# 2️⃣ Siempre loggear la excepción con información relevante
# 3️⃣ Retornar valores de fallback solo si tiene sentido
# 4️⃣ Re-lanzar excepciones inesperadas para no ocultar fallos graves
# 5️⃣ Mantener consistencia en todo el pipeline de errores
# 6️⃣ Swallow exceptions solo en casos muy controlados, documentados y con fallback seguro
# 7️⃣ Usar bloques específicos de except para cada tipo de excepción esperada
