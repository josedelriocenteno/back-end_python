"""
isort.py
========

Este archivo enseña cómo usar **isort** para ordenar y organizar imports
automáticamente, manteniendo un estilo limpio y profesional en Python.

Beneficios:
- Imports consistentes en todo el proyecto
- Facilita leer dependencias
- Evita errores por imports duplicados o circulares
- Complementa Flake8, Pylint y Black
"""

# -------------------------------------------------------------------
# 1️⃣ INSTALACIÓN
# -------------------------------------------------------------------

# Desde terminal:
# pip install isort

# Para comprobar versión:
# isort --version

# Para analizar un archivo:
# isort mi_archivo.py --check-only

# Para formatear un archivo:
# isort mi_archivo.py

# Para formatear todo el proyecto:
# isort src/ tests/


# -------------------------------------------------------------------
# 2️⃣ IMPORTS DESORDENADOS
# -------------------------------------------------------------------

# ❌ MAL
import sys, os
from collections import deque, defaultdict
import numpy as np
from myproject.utils import helper1, helper2
import pandas as pd
from django.db import models
from typing import List, Dict

# Problemas:
# - Mezcla imports estándar, terceros y locales
# - Sin orden alfabético
# - Difícil de mantener y leer


# -------------------------------------------------------------------
# 3️⃣ IMPORTS ORDENADOS MANUALMENTE (MEJOR)
# -------------------------------------------------------------------

# ✅ BIEN
# 1️⃣ Standard library
import os
import sys
from collections import deque, defaultdict

# 2️⃣ Third-party
import numpy as np
import pandas as pd
from django.db import models

# 3️⃣ Local application / project
from myproject.utils import helper1, helper2

# Ventaja:
# - Claro, predecible
# - Facilita encontrar dependencias
# - Evita errores de import duplicado


# -------------------------------------------------------------------
# 4️⃣ ISORT FORMATEA AUTOMÁTICAMENTE
# -------------------------------------------------------------------

# Ejecutar:
# isort mi_archivo.py

# Resultado:
"""
import os
import sys
from collections import deque, defaultdict

import numpy as np
import pandas as pd
from django.db import models

from myproject.utils import helper1, helper2
"""


# -------------------------------------------------------------------
# 5️⃣ CONFIGURACIÓN RECOMENDADA (pyproject.toml)
# -------------------------------------------------------------------

"""
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
combine_as_imports = true
known_first_party = ["myproject"]
known_third_party = ["numpy", "pandas", "django"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
skip = [".venv", "build", "dist"]
"""

# Explicación:
# - `profile = "black"`: compatible con Black
# - `sections`: separa imports por tipo (estándar, terceros, locales)
# - `known_first_party` / `known_third_party`: ayuda a clasificar correctamente
# - `skip`: carpetas que no se analizan


# -------------------------------------------------------------------
# 6️⃣ INTEGRACIÓN EN PRE-COMMIT
# -------------------------------------------------------------------

# Pre-commit hook recomendado:
"""
repos:
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
"""

# Así se asegura que todos los imports estén ordenados antes de subir código


# -------------------------------------------------------------------
# 7️⃣ REGLAS DE ORO
# -------------------------------------------------------------------

# 1. Siempre separar imports por tipo: stdlib / terceros / locales
# 2. Orden alfabético dentro de cada sección
# 3. Mantener consistencia con Black (profile = "black")
# 4. Integrar en pre-commit para consistencia automática
# 5. Evitar importar múltiples módulos en la misma línea
# 6. Evitar imports circulares revisando dependencias locales


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------

# isort = estándar profesional para mantener imports limpios
# Combinado con Flake8, Pylint y Black:
# - Código consistente
# - Legible
# - Mantenible
# - Preparado para producción y equipos grandes
