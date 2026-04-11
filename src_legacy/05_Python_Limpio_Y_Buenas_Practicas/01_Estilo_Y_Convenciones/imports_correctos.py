"""
imports_correctos.py
====================

Este archivo explica el ORDEN correcto de imports en Python
y las buenas prácticas que evitan errores, acoplamiento y caos.

Los imports no son un detalle:
- afectan a la legibilidad
- afectan a la arquitectura
- afectan al arranque del programa
"""

# -------------------------------------------------------------------
# 1️⃣ ORDEN CORRECTO DE IMPORTS (REGLA OFICIAL)
# -------------------------------------------------------------------
#
# Los imports se agrupan en TRES bloques, separados por una línea en blanco:
#
# 1. Librería estándar de Python
# 2. Librerías externas (pip)
# 3. Código propio del proyecto
#
# Dentro de cada bloque: orden alfabético


# -------------------------------------------------------------------
# 2️⃣ EJEMPLO CORRECTO
# -------------------------------------------------------------------

# 1. Librería estándar
import math
from decimal import Decimal
from typing import List

# 2. Librerías externas
import numpy as np
import pandas as pd

# 3. Código propio
from domain.entities.usuario import Usuario
from domain.services.pedido_service import PedidoService


# -------------------------------------------------------------------
# 3️⃣ EJEMPLO INCORRECTO (MUY COMÚN)
# -------------------------------------------------------------------

# ❌ MAL
# import numpy as np
# from domain.entities.usuario import Usuario
# import math
# import pandas as pd
# from decimal import Decimal

# Problemas:
# - el orden no es predecible
# - cuesta leer
# - dificulta code reviews


# -------------------------------------------------------------------
# 4️⃣ IMPORTS ESPECÍFICOS VS IMPORT *
# -------------------------------------------------------------------

# ❌ MAL
# from math import *

# ¿Por qué es malo?
# - no sabes qué se importa
# - puede sobrescribir nombres
# - rompe herramientas de análisis


# ✅ BIEN
from math import sqrt, ceil

# Ahora:
# - sabes exactamente qué usas
# - no hay sorpresas
# - el código es explícito


# -------------------------------------------------------------------
# 5️⃣ ALIAS: CUÁNDO USARLOS
# -------------------------------------------------------------------
#
# Los alias solo se usan cuando:
# - el nombre es largo
# - es una convención conocida

# ✅ BIEN
import numpy as np
import pandas as pd

# ❌ MAL
# import numpy as n
# import pandas as p


# -------------------------------------------------------------------
# 6️⃣ IMPORTS LOCALES (DENTRO DE FUNCIONES)
# -------------------------------------------------------------------
#
# Normalmente los imports van ARRIBA del archivo.
#
# Se permiten imports locales SOLO si:
# - evitan dependencias circulares
# - reducen tiempo de arranque
# - son opcionales

def calcular_raiz_segura(valor: float) -> float:
    """
    Ejemplo de import local justificado.
    """
    import math

    if valor < 0:
        raise ValueError("No se puede calcular la raíz de un número negativo")

    return math.sqrt(valor)


# -------------------------------------------------------------------
# 7️⃣ DEPENDENCIAS EXPLÍCITAS
# -------------------------------------------------------------------
#
# ❌ MAL
# from utils import *

# Nadie sabe qué necesita realmente este módulo.


# ✅ BIEN
from utils.validaciones import validar_email
from utils.fechas import obtener_fecha_actual


# -------------------------------------------------------------------
# 8️⃣ EVITAR IMPORTS CIRCULARES
# -------------------------------------------------------------------
#
# Síntoma:
# - ImportError extraño
# - atributos que "no existen"
#
# Causa:
# - módulos que dependen entre sí
#
# Soluciones:
# - mover interfaces a un módulo común
# - invertir dependencias
# - usar inyección de dependencias


# -------------------------------------------------------------------
# 9️⃣ IMPORTS Y HERRAMIENTAS AUTOMÁTICAS
# -------------------------------------------------------------------
#
# Herramientas como isort:
# - ordenan imports automáticamente
# - eliminan imports no usados
#
# Esto:
# - evita discusiones
# - mantiene el estilo consistente
#
# En equipos, el orden NO se decide a mano.


# -------------------------------------------------------------------
# 🔟 REGLA DE ORO
# -------------------------------------------------------------------
#
# Leyendo solo los imports de un archivo
# deberías entender:
# - de qué depende
# - qué responsabilidades tiene
#
# Si los imports parecen caóticos,
# el diseño probablemente también lo sea.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Imports limpios:
# - mejoran la lectura
# - reducen bugs
# - reflejan buena arquitectura
#
# No es burocracia.
# Es ingeniería.
