"""
black.py
========

Este archivo explica cómo usar **Black**, el formateador automático de código Python,
para mantener un estilo consistente y limpio en todo el proyecto.

Beneficios:
- Código consistente automáticamente
- Evita discusiones de estilo en revisiones de código
- Compatible con pre-commit y pipelines CI/CD
"""

# -------------------------------------------------------------------
# 1️⃣ INSTALACIÓN
# -------------------------------------------------------------------

# Desde terminal:
# pip install black

# Comprobar versión:
# black --version

# Formatear un archivo:
# black mi_archivo.py

# Formatear todo el proyecto:
# black src/ tests/ --line-length 88


# -------------------------------------------------------------------
# 2️⃣ EJEMPLO: CÓDIGO MAL FORMATEADO
# -------------------------------------------------------------------

# ❌ MAL
def funcion_mala(a:int,b:int)->int: return a+b

x=[1,2,3,4,5];y= [x**2 for x in x]; print(y)

class Producto: 
    def __init__(self,id,nombre,precio): self.id=id;self.nombre=nombre;self.precio=precio

# Problema:
# - Líneas demasiado largas
# - Espacios inconsistentes
# - Código difícil de leer y revisar


# -------------------------------------------------------------------
# 3️⃣ BLACK LO FORMATEA AUTOMÁTICAMENTE
# -------------------------------------------------------------------

# ✅ BIEN: después de black
def funcion_bien(a: int, b: int) -> int:
    return a + b


x = [1, 2, 3, 4, 5]
y = [x**2 for x in x]
print(y)


class Producto:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio


# -------------------------------------------------------------------
# 4️⃣ CONFIGURACIÓN RECOMENDADA
# -------------------------------------------------------------------

# Crear archivo pyproject.toml en la raíz del proyecto:

"""
[tool.black]
line-length = 88
target-version = ['py39']
skip-string-normalization = false
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
"""

# Esto asegura:
# - Líneas ≤ 88 caracteres
# - Compatibilidad con Python 3.9+
# - Normalización de comillas
# - Ignora carpetas de entorno virtual, build y dist


# -------------------------------------------------------------------
# 5️⃣ INTEGRACIÓN EN EL PROYECTO
# -------------------------------------------------------------------

# Formateo automático previo a commit con pre-commit:
# pip install pre-commit
# pre-commit install

# Configuración pre-commit:
"""
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
"""

# Con esto, Black formatea automáticamente todo el código antes de subirlo a git.


# -------------------------------------------------------------------
# 6️⃣ REGLAS DE ORO
# -------------------------------------------------------------------

# 1. No discutas estilo: usa Black para formateo automático
# 2. Configura line-length = 88 (PEP8 + legibilidad)
# 3. Integra en pre-commit para consistencia en todo el equipo
# 4. Combina Black + Flake8 + Pylint para máxima calidad
# 5. Usa Black en CI/CD para asegurar código limpio en producción


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------

# Black = formateo automático profesional
# Garantiza consistencia, legibilidad y reduce errores de estilo
# Combinado con linters y revisiones, tu código siempre será limpio y mantenible
