# coste_de_operaciones.py
"""
Coste de Operaciones en Python – Backend Profesional

Este módulo cubre:
- Cómo calcular el coste de diferentes operaciones
- Comparación de eficiencia en listas, diccionarios y sets
- Ejemplos prácticos para pipelines y backend
"""

import time

# -------------------------------------------------
# 1. Medir tiempo de ejecución de operaciones
# -------------------------------------------------
def medir_tiempo(funcion, *args):
    inicio = time.time()
    funcion(*args)
    fin = time.time()
    return fin - inicio

# -------------------------------------------------
# 2. Acceso a elementos
# -------------------------------------------------
numeros = list(range(1000000))
# O(1) - acceso por índice
def acceso_lista():
    for i in range(1000):
        x = numeros[500000]

print("Acceso lista O(1):", medir_tiempo(acceso_lista), "segundos")

# O(n) - búsqueda lineal
def busqueda_lineal():
    for i in range(1000):
        999999 in numeros

print("Búsqueda lineal O(n):", medir_tiempo(busqueda_lineal), "segundos")

# -------------------------------------------------
# 3. Inserción y búsqueda en diccionarios
# -------------------------------------------------
dic = {i: i for i in range(1000000)}

# Inserción O(1)
def insercion_dic():
    for i in range(1000):
        dic[i + 1000000] = i

print("Inserción dic O(1):", medir_tiempo(insercion_dic), "segundos")

# Búsqueda O(1)
def busqueda_dic():
    for i in range(1000):
        _ = dic.get(500000)

print("Búsqueda dic O(1):", medir_tiempo(busqueda_dic), "segundos")

# -------------------------------------------------
# 4. Sets – operaciones rápidas
# -------------------------------------------------
conjunto = set(range(1000000))

# O(1) membership test
def membership_set():
    for i in range(1000):
        500000 in conjunto

print("Membership set O(1):", medir_tiempo(membership_set), "segundos")

# -------------------------------------------------
# 5. Comparación de bucles anidados vs diccionarios
# -------------------------------------------------
lista1 = list(range(1000))
lista2 = list(range(1000))

# O(n^2) – nested loops
def nested_loops():
    for a in lista1:
        for b in lista2:
            _ = a == b

print("Nested loops O(n^2):", medir_tiempo(nested_loops), "segundos")

# O(n) – usando diccionario
dict2 = {x: True for x in lista2}
def loops_dic():
    for a in lista1:
        _ = dict2.get(a, False)

print("Loops con diccionario O(n):", medir_tiempo(loops_dic), "segundos")

# -------------------------------------------------
# 6. Buenas prácticas profesionales
# -------------------------------------------------
"""
- Evita nested loops si puedes usar sets o diccionarios
- Prefiere operaciones O(1) para búsqueda e inserción
- Siempre mide tiempo de ejecución si trabajas con datasets grandes
- Documenta operaciones críticas y su coste esperado
- Esto previene pipelines lentos y problemas de escalabilidad
"""
