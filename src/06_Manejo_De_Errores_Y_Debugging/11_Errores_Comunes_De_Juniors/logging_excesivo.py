"""
logging_excesivo.py
====================

Objetivo:
- Mostrar los problemas de logging excesivo
- Enseñar cómo loggear de forma profesional y eficiente
"""

import logging

# -------------------------------------------------------------------
# 1️⃣ ANTI-PATRÓN: logging excesivo
# -------------------------------------------------------------------

def proceso_ruidoso():
    for i in range(5):
        logging.info(f"Iteración {i}: paso 1 completado")
        logging.info(f"Iteración {i}: paso 2 completado")
        logging.info(f"Iteración {i}: paso 3 completado")
        logging.debug(f"Iteración {i}: variable temporal x={i*2}")

# Problemas:
# - El log crece demasiado rápido
# - Difícil encontrar información relevante
# - Puede afectar rendimiento
# - Difícil filtrar errores críticos

# -------------------------------------------------------------------
# 2️⃣ FORMA PROFESIONAL: logging selectivo
# -------------------------------------------------------------------

def proceso_profesional():
    for i in range(5):
        # Log solo eventos importantes
        if i == 0:
            logging.info(f"Inicio del proceso, iteración {i}")
        if i == 4:
            logging.info(f"Final del proceso, iteración {i}")
        # Errores y warnings loguear siempre
        try:
            if i == 2:
                raise ValueError("Error simulado en iteración 2")
        except ValueError as e:
            logging.error(f"Excepción detectada: {e}", exc_info=True)

# -------------------------------------------------------------------
# 3️⃣ CONFIGURACIÓN PROFESIONAL
# -------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # DEBUG solo para desarrollo
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("Ejecutando proceso ruidoso (anti-patrón)...")
    proceso_ruidoso()

    print("\nEjecutando proceso profesional (logging claro)...")
    proceso_profesional()

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Loggear solo información útil y relevante
# 2️⃣ Separar niveles de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
# 3️⃣ DEBUG → desarrollo, INFO/WARNING/ERROR → producción
# 4️⃣ Evitar loggear cada paso trivial en loops grandes
# 5️⃣ Usar exc_info=True para capturar stack traces en errores
# 6️⃣ Centralizar configuración de logging para consistencia
# 7️⃣ Revisar logs periódicamente y ajustar niveles según necesidades
# 8️⃣ Mantener logs legibles y filtrables para debugging y auditoría
