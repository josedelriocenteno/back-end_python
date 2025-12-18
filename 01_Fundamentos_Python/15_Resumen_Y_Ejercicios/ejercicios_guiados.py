# ejercicios_guiados.py
"""
Ejercicios Guiados – Fundamentos Python
Nivel: Profesional / Backend / Data Pipelines

Objetivo:
- Aplicar sintaxis, tipos, estructuras, funciones y buenas prácticas
- Resolver problemas típicos de backend y manipulación de datos
- Practicar control de flujo, comprehensions y manejo de errores
"""

# -------------------------------------------------
# Ejercicio 1: Transformación de datos
# -------------------------------------------------
# Dada una lista de edades, generar una lista de booleanos indicando si son mayores de edad

edades = [12, 25, 18, 17, 30]

# Solución con list comprehension
mayores = [edad >= 18 for edad in edades]
print("Mayores de edad:", mayores)  # [False, True, True, False, True]

# -------------------------------------------------
# Ejercicio 2: Filtrado y map
# -------------------------------------------------
# De una lista de números, obtener los cuadrados de los pares

numeros = list(range(10))
cuadrados_pares = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numeros)))
print("Cuadrados pares:", cuadrados_pares)

# -------------------------------------------------
# Ejercicio 3: Diccionarios y lookup eficiente
# -------------------------------------------------
usuarios = [
    {"id": 1, "nombre": "Alice"},
    {"id": 2, "nombre": "Bob"},
    {"id": 3, "nombre": "Charlie"},
]

# Crear diccionario por id para búsquedas O(1)
usuarios_dict = {u["id"]: u for u in usuarios}
print("Usuario 2:", usuarios_dict[2]["nombre"])

# -------------------------------------------------
# Ejercicio 4: Manejo de errores
# -------------------------------------------------
datos = ["10", "5", "x", "20"]

def safe_int(s):
    try:
        return int(s)
    except ValueError:
        return None

enteros = [safe_int(d) for d in datos]
print("Convertidos a enteros:", enteros)  # [10, 5, None, 20]

# -------------------------------------------------
# Ejercicio 5: Funciones profesionales
# -------------------------------------------------
# Función que devuelve promedio de lista ignorando None

def promedio(lista):
    filtrados = [x for x in lista if x is not None]
    if not filtrados:
        return 0
    return sum(filtrados) / len(filtrados)

print("Promedio:", promedio(enteros))  # 11.666...

# -------------------------------------------------
# Ejercicio 6: Strings y f-strings
# -------------------------------------------------
nombres = ["Alice", "Bob", "Charlie"]
for i, nombre in enumerate(nombres, 1):
    print(f"{i}. Hola, {nombre}!")

# -------------------------------------------------
# Ejercicio 7: Iterables y comprehensions avanzadas
# -------------------------------------------------
# Generar diccionario {numero: cuadrado} solo para números pares

cuadrados_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print("Diccionario de cuadrados pares:", cuadrados_dict)

# -------------------------------------------------
# Ejercicio 8: Complejidad y eficiencia
# -------------------------------------------------
# Dadas dos listas, encontrar elementos comunes de forma eficiente

lista1 = list(range(1000))
lista2 = list(range(500, 1500))

# Ineficiente: O(n^2)
# comunes = [x for x in lista1 for y in lista2 if x == y]

# Eficiente: O(n)
set2 = set(lista2)
comunes = [x for x in lista1 if x in set2]
print("Elementos comunes (primeros 10):", comunes[:10])

# -------------------------------------------------
# Ejercicio 9: Buenas prácticas
# -------------------------------------------------
# Refactorizar función para modularidad y claridad

def procesar_lista(lista):
    """Filtra pares, calcula cuadrados y devuelve promedio"""
    pares = [x for x in lista if x % 2 == 0]
    cuadrados = [x**2 for x in pares]
    return promedio(cuadrados)

resultado = procesar_lista(list(range(10)))
print("Resultado procesamiento:", resultado)
