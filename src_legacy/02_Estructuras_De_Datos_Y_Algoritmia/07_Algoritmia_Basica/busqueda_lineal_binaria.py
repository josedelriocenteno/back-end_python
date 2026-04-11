# busqueda_lineal_binaria.py
"""
BÚSQUEDA LINEAL Y BINARIA EN PYTHON — CASOS DE USO REALES
=========================================================

Objetivo:
- Diferenciar búsqueda lineal vs binaria
- Elegir la técnica adecuada según datos y performance
- Aplicaciones en backend, pipelines y procesamiento de datos
"""

# ------------------------------------------------------------
# 1. BÚSQUEDA LINEAL
# ------------------------------------------------------------

# Características:
# - Lista no ordenada o pequeña
# - Simple y directa
# - O(n) tiempo de ejecución

def busqueda_lineal(lst, objetivo):
    for i, val in enumerate(lst):
        if val == objetivo:
            return i
    return -1

# Ejemplo real: buscar usuario en lista pequeña
usuarios = ["alice", "bob", "carol", "dave"]
idx = busqueda_lineal(usuarios, "carol")
print("Búsqueda lineal índice de carol:", idx)


# ------------------------------------------------------------
# 2. BÚSQUEDA BINARIA
# ------------------------------------------------------------

# Características:
# - Lista ordenada
# - Divide y vencerás → O(log n)
# - Mucho más rápida que lineal en listas grandes

def busqueda_binaria(lst, objetivo):
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == objetivo:
            return mid
        elif lst[mid] < objetivo:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Ejemplo real: buscar registro en tabla ordenada
ids = [101, 203, 305, 407, 509]
idx_bin = busqueda_binaria(ids, 305)
print("Búsqueda binaria índice de 305:", idx_bin)


# ------------------------------------------------------------
# 3. COMPARACIÓN DE USOS
# ------------------------------------------------------------

"""
| Método            | Datos ordenados | Complejidad | Uso recomendado               |
|------------------|----------------|------------|--------------------------------|
| Lineal            | No             | O(n)       | Listas pequeñas o desordenadas|
| Binaria           | Sí             | O(log n)   | Listas grandes y ordenadas    |
"""

# Escenario real: logs por usuario
# Log entries desordenadas → búsqueda lineal para few queries
# Log entries ordenadas por timestamp → búsqueda binaria


# ------------------------------------------------------------
# 4. TIPS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Ordena tu dataset si vas a hacer búsquedas frecuentes → binaria
✔ Lineal es suficiente para listas pequeñas (<100 elementos)
✔ Prefiere bisect module para búsquedas binarias con insert automáticos
✔ Evita bucles anidados con búsquedas lineales → O(n^2) peligroso
"""

import bisect

# Ejemplo avanzado: bisect
lista_ordenada = [10, 20, 30, 40, 50]
pos = bisect.bisect_left(lista_ordenada, 35)  # dónde insertar 35
print("Posición insert con bisect:", pos)


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar lineal en listas grandes → cuellos de botella
❌ Olvidar que binaria requiere lista ordenada
❌ Implementar binaria mal → errores de índices
❌ No usar bisect para insert/search eficiente
"""

print("Búsqueda lineal y binaria comprendidas profesionalmente")
