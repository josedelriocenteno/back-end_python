"""
estructura_archivos.py
======================

Este archivo explica CÓMO organizar archivos, módulos y paquetes en Python.

La estructura de un proyecto NO es un detalle estético:
- afecta a la mantenibilidad
- afecta a la escalabilidad
- afecta a cómo piensa el equipo

Un proyecto mal organizado:
- se vuelve inmanejable
- genera imports caóticos
- crea dependencias ocultas
"""

# -------------------------------------------------------------------
# 1️⃣ ¿QUÉ ES UN MÓDULO?
# -------------------------------------------------------------------
#
# En Python:
# - un archivo .py = un módulo
# - su nombre importa
#
# El módulo debe tener una RESPONSABILIDAD clara.
#
# ❌ MAL:
# utils.py  (contiene de todo)
#
# ✅ BIEN:
# fechas.py
# validaciones.py
# calculos_precios.py


# -------------------------------------------------------------------
# 2️⃣ ¿QUÉ ES UN PAQUETE?
# -------------------------------------------------------------------
#
# Un paquete es un directorio que agrupa módulos relacionados.
#
# Estructura típica:
#
# proyecto/
# ├── domain/
# │   ├── entities/
# │   │   ├── usuario.py
# │   │   └── pedido.py
# │   ├── value_objects/
# │   │   └── id_value.py
# │   └── services/
# │       └── pedido_service.py
#
# Cada nivel añade CONTEXTO.
# No redundancia.


# -------------------------------------------------------------------
# 3️⃣ ESTRUCTURA PLANA vs ESTRUCTURA POR CAPAS
# -------------------------------------------------------------------

# ❌ MAL: todo en el mismo nivel
#
# proyecto/
# ├── usuario.py
# ├── pedido.py
# ├── service.py
# ├── utils.py
# ├── helpers.py
#
# Problemas:
# - nadie sabe dónde va cada cosa
# - imports cruzados
# - caos progresivo


# ✅ BIEN: estructura por responsabilidad
#
# proyecto/
# ├── domain/
# │   ├── entities/
# │   ├── value_objects/
# │   └── services/
# ├── infrastructure/
# │   ├── database/
# │   └── repositories/
# ├── application/
# │   └── use_cases/
# └── main.py


# -------------------------------------------------------------------
# 4️⃣ ¿CÓMO DECIDIR DÓNDE VA UN ARCHIVO?
# -------------------------------------------------------------------
#
# Pregunta clave:
# 👉 ¿QUÉ PROBLEMA resuelve este código?
#
# - reglas de negocio → domain/
# - acceso a datos → repositories / infrastructure
# - lógica de aplicación → application
# - entrada/salida (API, CLI) → main / interfaces


# -------------------------------------------------------------------
# 5️⃣ IMPORTS LIMPIOS Y PREDECIBLES
# -------------------------------------------------------------------

# ❌ MAL: imports relativos profundos
# from ....utils.helpers import funcion

# ❌ MAL: imports circulares
# usuario importa pedido
# pedido importa usuario

# ✅ BIEN: imports claros y estables
from domain.entities.usuario import Usuario
from domain.services.pedido_service import PedidoService


# -------------------------------------------------------------------
# 6️⃣ __init__.py (CUÁNDO USARLO)
# -------------------------------------------------------------------
#
# __init__.py permite:
# - marcar un directorio como paquete
# - exponer una API limpia del paquete

# Ejemplo:
#
# domain/entities/__init__.py
# ---------------------------
# from .usuario import Usuario
# from .pedido import Pedido
#
# Uso:
# from domain.entities import Usuario, Pedido


# -------------------------------------------------------------------
# 7️⃣ EVITAR DEPENDENCIAS CIRCULARES
# -------------------------------------------------------------------
#
# Síntoma típico:
# - errores raros de import
# - código que solo funciona en cierto orden
#
# Causa:
# - mala separación de responsabilidades
#
# Solución:
# - extraer interfaces
# - mover dependencias a capas superiores
# - usar inyección de dependencias


# -------------------------------------------------------------------
# 8️⃣ ESTRUCTURA PARA DATA / IA
# -------------------------------------------------------------------
#
# En proyectos de Data / ML:
#
# proyecto/
# ├── data/
# │   ├── raw/
# │   ├── processed/
# │   └── features/
# ├── pipelines/
# │   ├── ingestion.py
# │   ├── preprocessing.py
# │   └── training.py
# ├── models/
# │   └── modelo_v1.pkl
# └── experiments/


# Separar datos, código y modelos
# NO es opcional en ML.


# -------------------------------------------------------------------
# 9️⃣ ARCHIVOS DEMASIADO GRANDES
# -------------------------------------------------------------------
#
# Regla práctica:
# - si un archivo supera ~300-500 líneas
# - probablemente hace demasiadas cosas
#
# Mejor:
# - dividir por responsabilidad
# - no por tamaño arbitrario


# -------------------------------------------------------------------
# 🔟 REGLA DE ORO
# -------------------------------------------------------------------
#
# Si no sabes dónde poner un archivo:
# 👉 el diseño aún no está claro
#
# No lo escondas en utils.py.
# Replantea la estructura.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# La estructura del proyecto:
# - comunica intención
# - reduce errores
# - facilita el trabajo en equipo
#
# Un buen diseño se nota
# antes de leer una sola línea de código.
