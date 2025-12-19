# errores_bucles_comunes.py
"""
ERRORES COMUNES EN BUCLES
=========================

Objetivo:
- Identificar y evitar bucles infinitos
- Prevenir mutaciones peligrosas de estructuras
- Mejorar calidad y estabilidad del código en backend y pipelines de datos
"""

# =========================================================
# 1. BUCLES INFINITOS
# =========================================================

# ❌ Olvidar actualizar la condición
contador = 0
# while contador < 5:
#     print(contador)  # Esto sería bucle infinito

# ✅ Actualizar correctamente la condición
contador = 0
while contador < 5:
    print(contador)
    contador += 1

# =========================================================
# 2. MODIFICAR LISTAS DURANTE ITERACIÓN
# =========================================================

numeros = [1, 2, 3, 4, 5]

# ❌ Mutación peligrosa: eliminar mientras se itera
for n in numeros:
    if n % 2 == 0:
        numeros.remove(n)  # Puede saltarse elementos

# ✅ Usar comprensión de listas o iterar sobre copia
numeros = [1, 2, 3, 4, 5]
numeros_filtrados = [n for n in numeros if n % 2 != 0]
print(numeros_filtrados)

# =========================================================
# 3. USO INCORRECTO DE RANGE
# =========================================================

# ❌ Cambiar la lista mientras se usa range(len(lista)) puede romper indices
lista = [0, 1, 2, 3]
for i in range(len(lista)):
    lista.pop(i)  # Problema: modifica tamaño de lista

# ✅ Iterar sobre copia de indices o elementos
lista = [0, 1, 2, 3]
for i in range(len(lista)-1, -1, -1):  # iteración inversa
    lista.pop(i)

# =========================================================
# 4. BUENAS PRÁCTICAS
# =========================================================

# - Verificar siempre la condición del while
# - Evitar mutaciones de listas/diccionarios durante iteración
# - Preferir for sobre while cuando el número de iteraciones es conocido
# - Mantener el bucle limpio y conciso, delegar lógica compleja a funciones

# =========================================================
# 5. CASOS PROFESIONALES
# =========================================================

# Backend/data: procesamiento de registros, filtrado de streams, pipelines
data_stream = [1, 2, 3, 4, 5]
index = 0
while index < len(data_stream):
    valor = data_stream[index]
    print(f"Procesando: {valor}")
    index += 1
