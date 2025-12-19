# stack_frames.py
"""
STACK FRAMES EN PYTHON
======================

Objetivo:
- Comprender cómo Python maneja las llamadas a funciones mediante el stack de frames
- Entender el lifetime de variables y la resolución de scope
- Fundamental para debugging, optimización y diseño de pipelines robustos

Conceptos clave:
- Cada vez que se llama a una función, Python crea un "frame" en la pila de ejecución.
- El frame contiene:
  - Variables locales
  - Referencia a la función
  - Dirección de retorno
- Cuando la función termina, el frame se elimina y se libera memoria
- Stack frames permiten recursion, manejo de excepciones y closures
"""

# =========================================================
# 1. Ejemplo básico de stack frame
# =========================================================

def funcion_a():
    x = 10  # variable local en frame de funcion_a
    print("Dentro de funcion_a, x =", x)
    funcion_b()  # llamada a otra función crea nuevo frame

def funcion_b():
    y = 20  # variable local en frame de funcion_b
    print("Dentro de funcion_b, y =", y)

funcion_a()
# Cuando funcion_b termina, su frame desaparece
# funcion_b() fuera de funcion_a funcionaría, pero x no es accesible aquí

# =========================================================
# 2. Stack frames y recursion
# =========================================================

def factorial(n: int) -> int:
    """
    Calcula factorial de manera recursiva
    Cada llamada crea un frame nuevo
    """
    if n == 0:
        return 1
    return n * factorial(n-1)

print(factorial(5))  # 120

# Concepto:
# Stack frames se apilan y luego se desapilan en orden inverso

# =========================================================
# 3. Stack frames y scope/local/global
# =========================================================

x_global = 100

def ejemplo_scope():
    x_local = 50
    def inner():
        nonlocal x_local
        x_local += 1
        print("inner x_local:", x_local)
    inner()
    print("outer x_local:", x_local)
    print("global x_global:", x_global)

ejemplo_scope()

# =========================================================
# 4. Stack frames y debugging profesional
# =========================================================

# Herramientas:
# - pdb (Python Debugger)
# - IDEs como VSCode, PyCharm permiten inspeccionar frames
# - Útil para:
#   - Ver variables locales en cada frame
#   - Analizar recursión y llamadas anidadas
#   - Detectar memory leaks y variables no liberadas

# =========================================================
# 5. Buenas prácticas en backend/pipelines
# =========================================================

# - Mantener funciones cortas para no saturar stack frames
# - Evitar recursion profunda, usar iteración o tail-recursion optimizada
# - Entender frames ayuda a manejar closures y factories correctamente
# - Evitar side-effects globales que confundan el contenido de frames
# - Al procesar pipelines de datos grandes, cuidar el scope para liberar memoria
