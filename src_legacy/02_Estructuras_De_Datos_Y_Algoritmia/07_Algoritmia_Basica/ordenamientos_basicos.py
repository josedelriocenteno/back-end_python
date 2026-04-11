# ordenamientos_basicos.py
"""
ORDENAMIENTOS BÁSICOS EN PYTHON — sorted(), key, ESTABILIDAD
=============================================================

Objetivo:
- Entender cómo ordenar listas de manera profesional
- Usar `sorted()` y `list.sort()` con key functions
- Aplicar ordenamiento estable en backend y pipelines
"""

# ------------------------------------------------------------
# 1. sorted() vs list.sort()
# ------------------------------------------------------------

# sorted() → devuelve nueva lista, no modifica original
numeros = [5, 2, 9, 1, 5, 6]
ordenada = sorted(numeros)
print("Original:", numeros)
print("Sorted():", ordenada)

# list.sort() → ordena in-place
numeros.sort()
print("List.sort() in-place:", numeros)


# ------------------------------------------------------------
# 2. KEY FUNCTION
# ------------------------------------------------------------

# Ordenar listas de tuplas por segundo elemento
personas = [("Alice", 30), ("Bob", 25), ("Carol", 35)]
ordenadas_edad = sorted(personas, key=lambda x: x[1])
print("Ordenadas por edad:", ordenadas_edad)

# Ordenar strings ignorando mayúsculas/minúsculas
nombres = ["alice", "Bob", "carol"]
orden_nombres = sorted(nombres, key=str.lower)
print("Orden nombres ignorando case:", orden_nombres)


# ------------------------------------------------------------
# 3. ESTABILIDAD DEL ORDENAMIENTO
# ------------------------------------------------------------

# Ordenamiento estable → mantiene el orden relativo de elementos iguales
datos = [("A", 3), ("B", 1), ("C", 3), ("D", 2)]
# Ordenar por segundo elemento
ordenado = sorted(datos, key=lambda x: x[1])
print("Orden estable:", ordenado)
# Nota: ("A",3) aparece antes que ("C",3) → mantiene orden original


# ------------------------------------------------------------
# 4. EJEMPLOS REALES BACKEND / DATA
# ------------------------------------------------------------

# Ordenar logs por timestamp
logs = [
    {"user": "alice", "time": "10:05"},
    {"user": "bob", "time": "10:03"},
    {"user": "carol", "time": "10:05"}
]
logs_ordenados = sorted(logs, key=lambda x: x["time"])
print("Logs ordenados por tiempo:", logs_ordenados)

# Ordenar usuarios por múltiples criterios
usuarios = [
    {"nombre": "Alice", "edad": 30},
    {"nombre": "Bob", "edad": 25},
    {"nombre": "Carol", "edad": 30}
]
# Primero por edad, luego por nombre (orden estable)
usuarios_ordenados = sorted(usuarios, key=lambda x: (x["edad"], x["nombre"]))
print("Usuarios ordenados por edad y nombre:", usuarios_ordenados)


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar sort sin key → errores en estructuras complejas
❌ Ignorar estabilidad → datos relacionados se mezclan
❌ Ordenar listas enormes in-place si necesitas mantener original
❌ No considerar eficiencia → sorted() O(n log n)
"""

# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Prefiere key function para ordenar dicts o tuplas
✔ Usa sorted() si quieres mantener lista original
✔ Ordenamiento estable siempre que dependas de orden previo
✔ Evita bucles para ordenar manualmente → siempre sort builtin
✔ Documenta criterio de ordenación en pipelines o APIs
"""

print("Ordenamientos básicos dominados profesionalmente")
