"""
logging_basico.py
=================

Objetivo:
- Entender por qué `logging` reemplaza a `print` en proyectos profesionales
- Aprender a configurar logging básico
- Diferenciar niveles de mensajes y uso apropiado
"""

# -------------------------------------------------------------------
# 1️⃣ PROBLEMA DE USAR print
# -------------------------------------------------------------------

# ❌ Print simple
print("Inicio del proceso")
print("Algo falló")
print("Proceso terminado")

# Problemas:
# 1. No hay niveles de severidad
# 2. Difícil filtrar mensajes en producción
# 3. No hay timestamp ni contexto
# 4. Difícil redirigir a archivo o sistema de monitoreo

# -------------------------------------------------------------------
# 2️⃣ USO BÁSICO DE logging
# -------------------------------------------------------------------

import logging

# Configuración básica
logging.basicConfig(
    level=logging.INFO,                # Nivel mínimo de logs a mostrar
    format="%(levelname)s - %(asctime)s - %(message)s"
)

logging.debug("Este mensaje no se verá porque level=INFO")
logging.info("Inicio del proceso")       # INFO
logging.warning("Advertencia: variable no usada")  # WARNING
logging.error("Error al procesar datos")          # ERROR
logging.critical("Fallo crítico del sistema")    # CRITICAL

# Output incluye:
# - Nivel
# - Timestamp
# - Mensaje
# Ejemplo:
# INFO - 2026-01-06 15:23:45,123 - Inicio del proceso

# -------------------------------------------------------------------
# 3️⃣ DIFERENCIAS CLAVE: print vs logging
# -------------------------------------------------------------------

# 1. Niveles de severidad: DEBUG, INFO, WARNING, ERROR, CRITICAL
# 2. Redirigible: consola, archivo, sistemas externos
# 3. Configurable: formato, filtros, timestamps
# 4. Profesional: permite monitoreo y mantenimiento
# 5. Print solo es útil para debugging rápido o scripts simples

# -------------------------------------------------------------------
# 4️⃣ EJEMPLO PROFESIONAL
# -------------------------------------------------------------------

def procesar_datos(data):
    if not data:
        logging.warning("Se recibió data vacía")
        return
    try:
        resultado = 10 / data
        logging.info(f"Resultado calculado: {resultado}")
    except ZeroDivisionError as e:
        logging.error(f"Error crítico al procesar datos: {e}")

procesar_datos(0)  # Genera log de error
procesar_datos(5)  # Genera log de info

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# 1. Usar logging en lugar de print en cualquier proyecto serio
# 2. Configurar niveles adecuados según entorno (DEBUG en dev, INFO/WARNING en prod)
# 3. Incluir timestamps y contexto (módulo, función, usuario si aplica)
# 4. Evitar prints residuales en código de producción
# 5. Combinar con try/except y fail-fast para errores profesionales
