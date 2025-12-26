# resumen_fundamentos.py
"""
Resumen de Fundamentos Python – Backend Profesional

Este archivo sirve como guía de referencia rápida para:
- Sintaxis y estructuras básicas
- Tipos de datos y conversiones
- Control de flujo y funciones
- Manejo de errores
- Módulos, paquetes y I/O
- Strings avanzados, iterables y comprehensions
- Funciones built-in clave y buenas prácticas
- Complejidad y rendimiento básico
"""

# -------------------------------------------------
# 1. Tipos de datos y conversiones
# -------------------------------------------------
edad = 25                   # int
precio = 19.99              # float
activo = True               # bool
nombre = "Backend Pro"      # str
nada = None                 # NoneType

# Conversiones
edad_str = str(edad)
precio_int = int(precio)

# -------------------------------------------------
# 2. Estructuras de datos
# -------------------------------------------------
lista = [1, 2, 3, 4]
tupla = (1, 2, 3)
conjunto = {1, 2, 3}
diccionario = {"nombre": "Alice", "edad": 30}

# Acceso y manipulación
lista.append(5)
diccionario["activo"] = True

# -------------------------------------------------
# 3. Control de flujo
# -------------------------------------------------
# Condicionales
if edad > 18:
    print("Adulto")
else:
    print("Menor")

# Bucles
for n in lista:
    print(n)

i = 0
while i < 5:
    i += 1

# Break, continue, pass
for n in lista:
    if n == 3:
        continue
    print(n)

# -------------------------------------------------
# 4. Funciones
# -------------------------------------------------
def suma(a, b):
    """Suma dos números"""
    return a + b

resultado = suma(5, 10)

# Argumentos posicionales y nominales
def saludar(nombre, mensaje="Hola"):
    print(f"{mensaje} {nombre}")

saludar("Alice")
saludar("Bob", mensaje="Bienvenido")

# -------------------------------------------------
# 5. Manejo de errores
# -------------------------------------------------
try:
    division = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("Finalizado")

# -------------------------------------------------
# 6. Módulos y paquetes
# -------------------------------------------------
import math
from datetime import datetime

raiz = math.sqrt(16)
hoy = datetime.now()

# -------------------------------------------------
# 7. Input/Output
# -------------------------------------------------
# Lectura/escritura archivos
with open("archivo.txt", "w") as f:
    f.write("Backend Pro")

with open("archivo.txt", "r") as f:
    contenido = f.read()

# -------------------------------------------------
# 8. Strings avanzados
# -------------------------------------------------
nombre = "Alice"
saludo = f"Hola {nombre}"       # f-strings
sub = nombre[0:3]               # slicing
longitud = len(nombre)
upper = nombre.upper()

# -------------------------------------------------
# 9. Iterables y comprehensions
# -------------------------------------------------
# List comprehension
cuadrados = [x**2 for x in range(10)]
# Dict comprehension
mapa = {x: x**2 for x in range(5)}
# Set comprehension
conjunto = {x for x in range(5)}

# -------------------------------------------------
# 10. Funciones built-in clave
# -------------------------------------------------
numeros = [1, 2, 3, 4, 5]
suma_total = sum(numeros)
max_val = max(numeros)
min_val = min(numeros)
existe_par = any(n % 2 == 0 for n in numeros)
todos_positivos = all(n > 0 for n in numeros)
pares = list(filter(lambda x: x % 2 == 0, numeros))
doble = list(map(lambda x: x*2, numeros))

# -------------------------------------------------
# 11. Complejidad y rendimiento básico
# -------------------------------------------------
# O(1) - acceso a índice
x = numeros[2]
# O(n) - recorrer lista
for n in numeros:
    pass
# O(n^2) - nested loops
for a in numeros:
    for b in numeros:
        pass

# -------------------------------------------------
# 12. Buenas prácticas
# -------------------------------------------------
# Código modular, legible y mantenible
# Funciones pequeñas, nombres claros
# Evitar código spaghetti y variables globales
# Usar linters y formateadores (black, flake8)
# Documentar decisiones críticas
