# control_flujo_vs_datos.py
"""
CONTROL DE FLUJO VS MANIPULACIÓN DE DATOS
=========================================

Objetivo:
- Diferenciar claramente cuándo estás controlando la lógica
  vs. cuándo estás transformando o manipulando datos.
- Concepto clave para backend y pipelines de datos.
"""

# =========================================================
# 1. CONTROL DE FLUJO
# =========================================================

# El control de flujo decide **qué hacer y cuándo**.
# No modifica datos por sí mismo, solo altera la ejecución.

x = 10
y = 5

# Ejemplo de control de flujo:
if x > y:
    print("x es mayor que y")
else:
    print("x no es mayor que y")

for i in range(3):
    if i % 2 == 0:
        continue  # salto de iteración
    print(f"i impar: {i}")

# break, continue, return, raise son control de flujo

# =========================================================
# 2. MANIPULACIÓN DE DATOS
# =========================================================

# Transformación o creación de datos.
# La lógica de control no cambia, solo los datos cambian.

numeros = [1, 2, 3, 4, 5]

# Ejemplo: map y list comprehension
cuadrados = [n**2 for n in numeros]  # manipula datos
print(cuadrados)

# Otra forma: filter
pares = list(filter(lambda n: n % 2 == 0, numeros))
print(pares)

# =========================================================
# 3. DIFERENCIA CLAVE
# =========================================================

"""
- Control de flujo: decide *la ruta de ejecución*
- Manipulación de datos: decide *el contenido de los datos*

Errores típicos de juniors:
1. Mezclar bucles de control con demasiada manipulación → código ilegible
2. Usar break/continue para "arreglar" lógica de transformación
3. No separar funciones puras de efectos secundarios
"""

# =========================================================
# 4. BUENAS PRÁCTICAS
# =========================================================

"""
- Separar funciones de transformación de datos de la lógica de flujo
- Funciones puras para datos → más fácil de testear y escalar
- Control de flujo explícito y mínimo → más legible
- Para backend: endpoints deciden flujo, funciones deciden transformación
"""

def procesar_datos(data):
    # transformación pura
    return [x*2 for x in data if x > 2]

entrada = [1,2,3,4]
salida = procesar_datos(entrada)
print(f"Entrada: {entrada} -> Salida: {salida}")

# =========================================================
# 5. RESUMEN PROFESIONAL
# =========================================================

"""
- Control de flujo: if, for, while, break, continue, raise, return
- Manipulación de datos: operaciones sobre estructuras, map/filter, comprehensions
- Regla: separa la lógica de control de la manipulación de datos
- Backend/Data: endpoints y pipelines claros y testables
"""
