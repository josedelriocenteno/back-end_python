#!/bin/bash
# Archivo: Automatizacion_basica.sh
# Propósito: Automatizar tareas comunes de un proyecto backend Python
# Nivel: Profesional
# Notas: Este script sirve tanto como flujo de trabajo real como apuntes prácticos

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

# Activar modo estricto para detener el script si algún comando falla
set -e

# Variables configurables
ENV=".venv"            # Carpeta del entorno virtual
LOG_DIR="logs"         # Carpeta donde se guardan logs
PROJECT_DIR="$(pwd)"   # Directorio raíz del proyecto

# ============================================
# FUNCIONES PRINCIPALES
# ============================================

# Función: Activar entorno virtual
activar_entorno() {
    echo "=== Activando entorno virtual ==="
    if [ -d "$ENV" ]; then
        source "$ENV/bin/activate"
    else
        echo "Entorno virtual no encontrado, creando uno nuevo..."
        python3 -m venv "$ENV"
        source "$ENV/bin/activate"
    fi
}

# Función: Instalar dependencias
instalar_dependencias() {
    echo "=== Instalando dependencias ==="
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "No se encontró requirements.txt, saltando instalación."
    fi
}

# Función: Ejecutar tests
ejecutar_tests() {
    echo "=== Ejecutando tests unitarios ==="
    pytest tests/ --maxfail=5 --disable-warnings
}

# Función: Limpiar logs antiguos
limpiar_logs() {
    echo "=== Limpiando logs antiguos ==="
    if [ -d "$LOG_DIR" ]; then
        rm -rf "$LOG_DIR"/*.log
    else
        echo "Directorio de logs no existe, creando..."
        mkdir "$LOG_DIR"
    fi
}

# Función: Levantar servidor de desarrollo
levantar_servidor() {
    echo "=== Iniciando servidor FastAPI ==="
    uvicorn app.main:app --reload
}

# ============================================
# FLUJO PRINCIPAL DEL SCRIPT
# ============================================

# 1. Activar entorno virtual
activar_entorno

# 2. Instalar dependencias
instalar_dependencias

# 3. Ejecutar tests
ejecutar_tests

# 4. Limpiar logs
limpiar_logs

# 5. Levantar servidor
levantar_servidor

# ============================================
# FIN DEL SCRIPT
# ============================================
