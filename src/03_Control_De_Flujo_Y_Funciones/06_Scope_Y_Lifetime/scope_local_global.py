# scope_local_global.py
"""
SCOPE Y LIFETIME EN PYTHON
==========================

Objetivo:
- Comprender los alcances (scope) de las variables: local, global y nonlocal
- Evitar errores típicos de confusión de scope en backend, pipelines y data processing
- Esencial para funciones, closures y arquitecturas limpias

Contexto:
- Scope: dónde es visible una variable
- Lifetime: cuánto tiempo existe una variable en memoria
- Tipos de scope en Python:
  - Local: dentro de la función
  - Enclosing / Nonlocal: dentro de una función contenedora
  - Global: módulo actual
  - Built-in: funciones y objetos integrados
"""

# =========================================================
# 1. Scope local
# =========================================================

def ejemplo_local():
    x = 10  # variable local
    print("Local x:", x)

ejemplo_local()
# print(x)  # ❌ Error: x no existe fuera de la función

# =========================================================
# 2. Scope global
# =========================================================

y = 50  # variable global

def ejemplo_global():
    global y
    y += 10  # modificando variable global
    print("Dentro de la función, y =", y)

print("Antes de función, y =", y)
ejemplo_global()
print("Después de función, y =", y)

# Nota: usar global con moderación; puede complicar pruebas y mantenimiento

# =========================================================
# 3. Scope nonlocal (enclosing)
# =========================================================

def contador():
    n = 0  # variable de enclosing scope

    def incrementar():
        nonlocal n  # se refiere a n de la función externa
        n += 1
        return n

    return incrementar

c = contador()
print(c())  # 1
print(c())  # 2
print(c())  # 3

# =========================================================
# 4. Scope en loops y comprehensions
# =========================================================

# En Python 3, variables de loops no contaminan el scope global
for i in range(3):
    pass
# print(i)  # ❌ NameError

# Comprehensions tienen su propio scope:
lista = [x for x in range(5)]
# print(x)  # ❌ NameError

# =========================================================
# 5. Buenas prácticas en backend/pipelines
# =========================================================

# - Evitar usar variables globales salvo en configuración o constantes
# - Usar parámetros y retornos para pasar información entre funciones
# - Nonlocal útil en closures y factories, pero documentar bien
# - Evitar sobrescribir variables externas accidentalmente
# - Mantener scope lo más local posible para claridad y testabilidad
