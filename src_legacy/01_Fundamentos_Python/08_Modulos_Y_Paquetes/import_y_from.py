# import_y_from.py
"""
Import y From en Python – Nivel Profesional Backend

Este módulo cubre:
- Diferencias entre `import` y `from`
- Cómo organizar imports en proyectos grandes
- Buenas prácticas para mantener código limpio
- Errores comunes y cómo evitarlos
"""

# -------------------------------------------------
# 1. import completo
# -------------------------------------------------
import math

resultado = math.sqrt(16)
print(resultado)  # 4.0

# ✔️ Ventaja: namespace completo, evita conflictos de nombres
# ❌ Desventaja: verbose si se usan muchas funciones


# -------------------------------------------------
# 2. from … import … 
# -------------------------------------------------
from math import sqrt, pi

resultado = sqrt(25)
print(resultado)  # 5.0
print(pi)         # 3.14159...

# ✔️ Ventaja: más conciso
# ❌ Desventaja: posibles conflictos si nombres se repiten


# -------------------------------------------------
# 3. from … import * 
# -------------------------------------------------
from math import *

# ❌ No recomendado en backend profesional
# - Contamina el namespace
# - Dificulta mantenimiento
# - Puede causar bugs silenciosos
resultado = sqrt(36)
print(resultado)


# -------------------------------------------------
# 4. Alias con as
# -------------------------------------------------
import numpy as np
from datetime import datetime as dt

array = np.array([1,2,3])
ahora = dt.now()
print(array, ahora)


# -------------------------------------------------
# 5. Organización de imports profesional
# -------------------------------------------------
# Orden recomendado por PEP8:
# 1. Librerías estándar (math, os, sys)
# 2. Librerías de terceros (numpy, pandas)
# 3. Módulos internos del proyecto
# Separar bloques con línea en blanco

import os
import sys

import numpy as np
import pandas as pd

from backend.utils import helper_function


# -------------------------------------------------
# 6. Evitar imports circulares
# -------------------------------------------------
# ❌ Malo: módulo A importa B y B importa A → error runtime
# ✔️ Profesional:
# - Reorganizar funciones en módulos
# - Usar imports dentro de funciones si es necesario


# -------------------------------------------------
# 7. Errores comunes de juniors
# -------------------------------------------------
# ❌ Usar from … import * 
# ❌ Confundir import absoluto y relativo
# ❌ Mezclar demasiados alias confusos
# ❌ No seguir PEP8 → imports desordenados


# -------------------------------------------------
# 8. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Imports claros y organizados
# ✔️ Evitar * import
# ✔️ Usar alias solo cuando mejora legibilidad
# ✔️ Imports relativos solo dentro de paquetes
# ✔️ Seguir PEP8 siempre


# -------------------------------------------------
# 9. Checklist mental backend
# -------------------------------------------------
# ✔️ Imports claros y legibles?  
# ✔️ Namespace controlado?  
# ✔️ Evitar conflictos de nombres?  
# ✔️ Siguiendo PEP8?  
# ✔️ Fácil de mantener y escalar?


# -------------------------------------------------
# 10. Regla de oro
# -------------------------------------------------
"""
Un backend profesional importa y organiza módulos con claridad:
- Evita conflictos de nombres
- Facilita mantenimiento
- Hace el código escalable y limpio
"""
