# errores_algoritmicos_comunes.py
"""
ERRORES ALGORÍTMICOS COMUNES EN PYTHON — CUELLOS DE BOTELLA
============================================================

Objetivo:
- Identificar errores típicos que afectan rendimiento
- Reconocer cuellos de botella en loops, listas, diccionarios y sets
- Aplicar buenas prácticas profesionales desde el inicio
"""

# ------------------------------------------------------------
# 1. USO INEFICIENTE DE BUCLES ANIDADOS
# ------------------------------------------------------------

# O(n^2) innecesario
numeros = list(range(1000))
pares = []
for x in numeros:
    for y in numeros:
        if x == y:
            pares.append((x, y))  # absurdo, O(n^2) sin necesidad

print("Ejemplo ineficiente (pares):", pares[:5])

# Solución: usar set intersection, comprehension o algoritmos adecuados
pares_opt = [(x, x) for x in numeros]  # O(n)
print("Ejemplo eficiente:", pares_opt[:5])


# ------------------------------------------------------------
# 2. MODIFICAR LISTAS DURANTE ITERACIÓN
# ------------------------------------------------------------

valores = [1, 2, 3, 4, 5]
for v in valores:
    if v % 2 == 0:
        valores.remove(v)  # error común: modifica lista mientras iteras

print("Lista modificada incorrectamente:", valores)

# Solución: crear nueva lista o usar comprehension
valores_correcto = [v for v in valores if v % 2 != 0]
print("Lista correcta:", valores_correcto)


# ------------------------------------------------------------
# 3. BÚSQUEDAS INEFICIENTES
# ------------------------------------------------------------

items = list(range(10000))

# Búsqueda lineal en lista grande → O(n)
if 9999 in items:
    print("Encontrado (lineal)")

# Solución profesional: usar set → O(1)
items_set = set(items)
if 9999 in items_set:
    print("Encontrado (set O(1))")


# ------------------------------------------------------------
# 4. USO INEFICIENTE DE CONCATENACIÓN DE STRINGS
# ------------------------------------------------------------

# Error común: concatenar en bucle → O(n^2)
textos = ["a"] * 1000
resultado = ""
for t in textos:
    resultado += t  # cada concatenación crea nueva string

print("Concatenación ineficiente:", resultado[:10])

# Solución: usar join → O(n)
resultado_eficiente = "".join(textos)
print("Concatenación eficiente:", resultado_eficiente[:10])


# ------------------------------------------------------------
# 5. SORTING INEFICIENTE
# ------------------------------------------------------------

datos = [5, 2, 9, 1, 5, 6]

# Evitar: burbuja o loops manuales → O(n^2)
# Correcto: usar sorted() o list.sort() → O(n log n)
datos_ordenados = sorted(datos)
print("Datos ordenados correctamente:", datos_ordenados)


# ------------------------------------------------------------
# 6. ERRORES DE MEMORIA
# ------------------------------------------------------------

# Crear listas gigantes sin necesidad → memoria extra
grande = [0] * 10**7  # puede ser ok, pero cuidado con entornos limitados

# Solución: usar generadores
grande_gen = (0 for _ in range(10**7))
print("Generador creado sin ocupar toda la memoria")


# ------------------------------------------------------------
# 7. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Analiza la complejidad O(n), O(n^2), O(log n) antes de implementar
✔ Evita modificar estructuras mientras iteras
✔ Prefiere sets/dicts para búsquedas rápidas
✔ Usa comprehensions y join para eficiencia y legibilidad
✔ Mantén código limpio y documentado
✔ Prueba tu algoritmo con datasets grandes
"""

print("Errores algorítmicos y cuellos de botella identificados profesionalmente")
