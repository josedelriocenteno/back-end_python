# flujo_ejecucion_programa.py
"""
FLUJO DE EJECUCIÓN EN PYTHON
============================

Objetivo:
- Entender cómo Python ejecuta código paso a paso
- Visualizar el orden, llamadas, imports y efectos secundarios
- Prepararte para depuración y diseño backend sólido
"""

# =========================================================
# 1. Python ejecuta de arriba a abajo
# =========================================================

print("Inicio del programa")

x = 10
y = 20

def suma(a, b):
    print(f"Llamando suma({a}, {b})")
    return a + b

resultado = suma(x, y)
print(f"Resultado: {resultado}")

# =========================================================
# 2. Importaciones
# =========================================================

# Cuando importas, Python ejecuta el módulo entero una vez.
# El código en el módulo se ejecuta al importarlo, no al usarlo.

import math  # solo se ejecuta una vez
import math  # Python usa el cache, no vuelve a ejecutar

# =========================================================
# 3. Funciones y scope
# =========================================================

# La función se define al leerla, pero no se ejecuta hasta que se llama.
def multiplicar(a, b):
    print(f"Llamando multiplicar({a}, {b})")
    return a * b

# =========================================================
# 4. Flujo con condicionales
# =========================================================

if resultado > 20:
    print("Resultado mayor que 20")
else:
    print("Resultado menor o igual a 20")

# =========================================================
# 5. Bucles y flujo
# =========================================================

for i in range(3):
    print(f"Iteración {i}")

# break y continue alteran el flujo normal
for i in range(5):
    if i == 2:
        continue  # salta a siguiente iteración
    if i == 4:
        break     # termina el bucle
    print(f"i = {i}")

# =========================================================
# 6. Llamadas anidadas y stack frames
# =========================================================

def f1():
    print("f1 start")
    f2()
    print("f1 end")

def f2():
    print("f2 start")
    f3()
    print("f2 end")

def f3():
    print("f3 start/end")

f1()

# =========================================================
# 7. Efectos secundarios y orden de ejecución
# =========================================================

# Las asignaciones, llamadas a funciones y prints
# siempre se ejecutan en el orden en que aparecen

# Concepto clave:
# - Python ejecuta instrucciones secuenciales
# - Llama a funciones solo cuando se invocan
# - Maneja el stack de llamadas automáticamente
# - Imports y ejecuciones top-level solo una vez

print("Fin del flujo de ejecución")

"""
Resumen rápido para backend/data:
- Todo lo que no está dentro de una función se ejecuta al importar o correr el módulo.
- Funciones y clases se definen pero no se ejecutan hasta que se llaman.
- El flujo puede alterarse con if, loops, break/continue, return.
- Cada llamada genera un stack frame: cuidado con recursión y efectos secundarios.
"""
