# complejidad_temporal.py
"""
COMPLEJIDAD TEMPORAL EN PYTHON — BIG-O EXPLICADO SIN HUMO
==========================================================

Objetivo:
- Entender la eficiencia de algoritmos y operaciones
- Evitar cuellos de botella en backend y procesamiento de datos
- Analizar coste temporal y espacial de estructuras y loops
"""

# ------------------------------------------------------------
# 1. CONCEPTOS BÁSICOS
# ------------------------------------------------------------

"""
- Big-O describe el crecimiento del tiempo de ejecución según el tamaño de entrada n
- No importa la máquina ni el lenguaje, sino el comportamiento asintótico
- Ejemplos comunes:
  O(1) → constante
  O(n) → lineal
  O(n^2) → cuadrática
  O(log n) → logarítmica
"""

# ------------------------------------------------------------
# 2. EJEMPLOS PRÁCTICOS
# ------------------------------------------------------------

# O(1) - Acceso a elemento de lista por índice
lista = [10, 20, 30, 40, 50]
print(lista[2])  # acceso directo

# O(n) - Búsqueda lineal
def busqueda_lineal(lst, objetivo):
    for x in lst:
        if x == objetivo:
            return True
    return False

print("Busqueda lineal 30:", busqueda_lineal(lista, 30))

# O(n^2) - Bucle anidado
def producto_cartesiano(lst1, lst2):
    result = []
    for x in lst1:
        for y in lst2:
            result.append((x, y))
    return result

print("Producto cartesiano:", producto_cartesiano([1,2], [3,4]))

# O(log n) - Búsqueda binaria (lista ordenada)
def busqueda_binaria(lst, objetivo):
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == objetivo:
            return True
        elif lst[mid] < objetivo:
            low = mid + 1
        else:
            high = mid - 1
    return False

print("Busqueda binaria 30:", busqueda_binaria(sorted(lista), 30))


# ------------------------------------------------------------
# 3. COSTE DE OPERACIONES COMUNES
# ------------------------------------------------------------

"""
- Acceso a lista por índice → O(1)
- Iterar lista → O(n)
- append() → O(1) amortizado
- insert() → O(n)
- pop() final → O(1)
- pop() inicio → O(n)
- diccionario get/set → O(1) promedio
- set add → O(1) promedio
- sorted() → O(n log n)
"""

# ------------------------------------------------------------
# 4. TIPS PRÁCTICOS PARA BACKEND
# ------------------------------------------------------------

"""
✔ Evita bucles anidados innecesarios
✔ Prefiere diccionarios o sets para búsquedas rápidas
✔ Analiza listas grandes → O(n^2) puede matar performance
✔ Considera algoritmos logarítmicos para datasets grandes
✔ Piensa en coste asintótico antes de pipeline o API lenta
"""

# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Ignorar complejidad y esperar que “funcione rápido”
❌ Confundir O(n) con O(1)
❌ Usar listas donde dicts o sets serían más eficientes
❌ No considerar crecimiento de n → problemas en producción
"""

print("Big-O y complejidad temporal comprendidos profesionalmente")
