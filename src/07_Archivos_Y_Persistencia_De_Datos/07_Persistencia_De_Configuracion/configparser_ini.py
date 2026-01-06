"""
configparser_ini.py
===================

GESTIÓN DE CONFIGURACIÓN CON ARCHIVOS INI EN PYTHON
---------------------------------------------------

Este archivo explica desde CERO:
- Qué es un archivo INI
- Por qué existe
- Cuándo usarlo
- Cómo leerlo correctamente en Python
- Qué problemas reales resuelve en proyectos medianos y grandes

Esto NO es teoría:
es configuración profesional.
"""

# ============================================================
# 1. EL PROBLEMA QUE RESUELVEN LOS ARCHIVOS INI
# ============================================================
# Ya sabemos que:
# - NO debemos hardcodear configuración
# - .env sirve para secretos simples
#
# Pero aparece un nuevo problema:
#
# ¿Qué pasa cuando la configuración es ESTRUCTURADA?
#
# Ejemplo:
# - Base de datos
# - Logging
# - Paths
# - Módulos
#
# Meter todo eso en un .env se vuelve caótico.
# ============================================================


# ============================================================
# 2. QUÉ ES UN ARCHIVO INI (DESDE CERO)
# ============================================================
# Un archivo INI es:
#
# - Un archivo de texto
# - Dividido en SECCIONES
# - Con pares clave = valor
#
# Ejemplo:
#
# [database]
# host = localhost
# port = 5432
#
# [logging]
# level = INFO
#
# Es LEGIBLE por humanos y máquinas.
# ============================================================


# ============================================================
# 3. CUÁNDO USAR INI VS .env (MUY IMPORTANTE)
# ============================================================
#
# .env:
# - Secretos
# - Variables simples
# - Sin estructura
#
# INI:
# - Configuración estructurada
# - Múltiples secciones
# - Proyectos medianos
#
# En proyectos reales:
# 👉 Se usan AMBOS.
# ============================================================


# ============================================================
# 4. LIBRERÍA configparser
# ============================================================
# Python trae configparser en la librería estándar.
# No hay que instalar nada.
# ============================================================

import configparser
from pathlib import Path


# ============================================================
# 5. RUTA DEL ARCHIVO DE CONFIGURACIÓN
# ============================================================
# Usamos pathlib:
# - portable
# - seguro
# - claro
# ============================================================

CONFIG_PATH = Path("config/app.ini")


# ============================================================
# 6. EJEMPLO DE ARCHIVO app.ini
# ============================================================
# (Esto NO es código, es cómo debería verse el archivo)
#
# [database]
# host = localhost
# port = 5432
# user = app_user
# password = secret
#
# [app]
# debug = true
# name = MiAplicacion
#
# ============================================================


# ============================================================
# 7. CARGAR EL ARCHIVO INI
# ============================================================

def cargar_configuracion(ruta: Path) -> configparser.ConfigParser:
    """
    Carga un archivo INI y devuelve el objeto ConfigParser.
    """

    config = configparser.ConfigParser()

    # read():
    # - Lee el archivo
    # - Parsea secciones y valores
    # - NO lanza error si falta (ojo)
    config.read(ruta)

    return config


# ============================================================
# 8. ACCEDER A VALORES DE CONFIGURACIÓN
# ============================================================

def leer_configuracion_basica(config: configparser.ConfigParser) -> None:
    """
    Muestra cómo acceder a valores.
    """

    # Acceso por sección y clave
    db_host = config["database"]["host"]
    db_port = config["database"]["port"]

    print("Host DB:", db_host)
    print("Puerto DB:", db_port)

    # IMPORTANTE:
    # configparser devuelve TODO como string
    # NO asume tipos
    # ========================================================


# ============================================================
# 9. CONVERSIÓN DE TIPOS (CRÍTICO)
# ============================================================

def leer_con_tipos(config: configparser.ConfigParser) -> None:
    """
    Lee valores convirtiéndolos a tipos correctos.
    """

    db_port = config.getint("database", "port")
    debug = config.getboolean("app", "debug")

    print("Puerto DB (int):", db_port)
    print("Debug (bool):", debug)


# ============================================================
# 10. POR QUÉ LOS TIPOS IMPORTAN
# ============================================================
#
# "5432" != 5432
#
# Comparaciones, cálculos, validaciones
# Todo puede romperse si no conviertes tipos.
#
# Este es un bug MUY común.
# ============================================================


# ============================================================
# 11. VALORES POR DEFECTO
# ============================================================

def leer_con_defaults(config: configparser.ConfigParser) -> None:
    """
    Lee valores con fallback si no existen.
    """

    timeout = config.getint(
        "network",
        "timeout",
        fallback=30  # segundos
    )

    print("Timeout:", timeout)


# ============================================================
# 12. VALIDAR CONFIGURACIÓN (NIVEL PRO)
# ============================================================
# Nunca asumas que el archivo está bien escrito.
# ============================================================

def validar_configuracion(config: configparser.ConfigParser) -> None:
    """
    Valida que existan secciones críticas.
    """

    secciones_requeridas = {"database", "app"}

    secciones_actuales = set(config.sections())

    faltantes = secciones_requeridas - secciones_actuales

    if faltantes:
        raise RuntimeError(
            f"Faltan secciones de configuración: {faltantes}"
        )


# ============================================================
# 13. ERROR TÍPICO DE JUNIORS
# ============================================================
#
# ❌ Acceder directamente sin validar
# ❌ Asumir que el archivo existe
# ❌ No convertir tipos
# ❌ Meter secretos aquí (mejor .env)
#
# ============================================================


# ============================================================
# 14. EJEMPLO COMPLETO
# ============================================================

def ejemplo_completo():
    config = cargar_configuracion(CONFIG_PATH)

    validar_configuracion(config)

    leer_configuracion_basica(config)
    leer_con_tipos(config)
    leer_con_defaults(config)


# ============================================================
# 15. IDEA FINAL CLAVE
# ============================================================
#
# configparser NO es solo para leer archivos.
#
# Es:
# - Contrato de configuración
# - Punto de entrada del sistema
# - Base de entornos reproducibles
#
# ============================================================


if __name__ == "__main__":
    ejemplo_completo()
