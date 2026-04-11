# errores_comunes_comprehensions.py
"""
Errores Comunes con List/Dict/Set Comprehensions – Backend Profesional

Este módulo cubre:
- Principales errores de juniors al usar comprehensions
- Cómo evitarlos
- Buenas prácticas profesionales
"""

# -------------------------------------------------
# 1. Comprehension demasiado larga
# -------------------------------------------------
numeros = [1,2,3,4,5,6,7,8,9,10]

# ❌ Complejo y difícil de leer
cuadrados_pares = [n**2 for n in numeros if n % 2 == 0 and n > 3 and n < 9 or n == 10]

# ✔️ Mejor dividir en pasos claros
cuadrados_pares = [n**2 for n in numeros if n % 2 == 0]
cuadrados_pares = [x for x in cuadrados_pares if 3 < x < 81 or x == 100]
print(cuadrados_pares)

# -------------------------------------------------
# 2. Efectos secundarios dentro de comprehensions
# -------------------------------------------------
# ❌ No hacer prints o modificar variables globales dentro
resultado = [print(n) for n in numeros]  # Malo en producción

# ✔️ Hacerlo en bucle separado
for n in numeros:
    print(n)

# -------------------------------------------------
# 3. Confusión entre list, dict y set comprehensions
# -------------------------------------------------
# ❌ Intentar usar dict comprehension pero olvidando pares key:value
lista = ["juan", "pedro"]
# diccionario_incorrecto = {x for x in lista}  # Error
diccionario_correcto = {x: len(x) for x in lista}  # Correcto
print(diccionario_correcto)

# ❌ Set comprehension esperando lista ordenada
set_incorrecto = {x**2 for x in numeros}  # OK, pero orden no garantizado
print(set_incorrecto)  # No preserva orden

# -------------------------------------------------
# 4. No usar filtrado interno
# -------------------------------------------------
# ❌ Filtrar fuera de la comprehension → más líneas de código
pares = []
for n in numeros:
    if n % 2 == 0:
        pares.append(n**2)

# ✔️ Filtrado dentro de comprehension
pares = [n**2 for n in numeros if n % 2 == 0]
print(pares)

# -------------------------------------------------
# 5. Uso excesivo de nested comprehensions
# -------------------------------------------------
# ❌ Difícil de leer y mantener
matriz = [[1,2],[3,4]]
flatten = [y for x in matriz for y in x if y % 2 == 0 and y != 4]

# ✔️ Mejor con bucle tradicional o dividir en pasos
flatten = []
for x in matriz:
    for y in x:
        if y % 2 == 0 and y != 4:
            flatten.append(y)
print(flatten)

# -------------------------------------------------
# 6. Errores comunes adicionales
# -------------------------------------------------
# ❌ Variables poco descriptivas
# ❌ Comprehensions con lógica compleja → ilegibles
# ❌ Mezclar tipos en una sola comprehension
# ❌ No testear casos límite

# -------------------------------------------------
# 7. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Mantener comprehensions simples y legibles
# ✔️ Filtrar y transformar dentro de la comprehension
# ✔️ Evitar efectos secundarios
# ✔️ Usar variables descriptivas
# ✔️ Dividir lógica compleja en pasos claros
# ✔️ Elegir la estructura correcta: list/dict/set

# -------------------------------------------------
# 8. Checklist mental backend
# -------------------------------------------------
# ✔️ Comprehensions legibles y seguras?  
# ✔️ Filtrado y transformación clara?  
# ✔️ Código limpio y mantenible?  
# ✔️ Evitando efectos secundarios?

# -------------------------------------------------
# 9. Regla de oro
# -------------------------------------------------
"""
En backend profesional:
- Comprehensions = concisas, claras y eficientes
- Evitar “magia” compleja que rompa legibilidad
- Siempre dividir pasos complejos para evitar errores
- Esto garantiza pipelines, APIs y data transformations robustas y profesionales
"""
