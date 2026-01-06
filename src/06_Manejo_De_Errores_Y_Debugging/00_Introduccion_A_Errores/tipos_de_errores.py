"""
tipos_de_errores.py
===================

Objetivo:
- Identificar los principales tipos de errores en Python
- Entender cuándo ocurren y cómo prevenirlos
"""

# -------------------------------------------------------------------
# 1️⃣ SYNTAX ERROR (Error de sintaxis)
# -------------------------------------------------------------------

# Qué es:
# - Python no puede interpretar el código
# - Ocurre en tiempo de compilación
# - Bloquea la ejecución del programa

# ❌ Ejemplo de código con SyntaxError
# def saludar()
#     print("Hola")  # falta ':' en la definición de la función

# ✅ Código correcto
def saludar():
    print("Hola")

saludar()  # Output: Hola

# -------------------------------------------------------------------
# 2️⃣ RUNTIME ERROR (Error en tiempo de ejecución)
# -------------------------------------------------------------------

# Qué es:
# - El código es sintácticamente correcto
# - Ocurre mientras se ejecuta el programa
# - Ejemplos: division por cero, acceso a índice inexistente, variable no definida

# ❌ ZeroDivisionError
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error en tiempo de ejecución: {e}")  # Output: division by zero

# ❌ IndexError
lista = [1, 2, 3]
try:
    print(lista[5])
except IndexError as e:
    print(f"Error en tiempo de ejecución: {e}")  # Output: list index out of range

# ❌ NameError
try:
    print(variable_inexistente)
except NameError as e:
    print(f"Error en tiempo de ejecución: {e}")  # Output: name 'variable_inexistente' is not defined

# -------------------------------------------------------------------
# 3️⃣ LOGICAL ERROR (Error lógico)
# -------------------------------------------------------------------

# Qué es:
# - El programa se ejecuta sin errores de sintaxis ni runtime
# - Pero produce resultados incorrectos
# - Generalmente culpa de la lógica del programador

# ❌ Ejemplo de error lógico: calcular promedio incorrecto
notas = [8, 9, 10]
promedio = sum(notas) / 2  # ❌ debería ser len(notas)
print(f"Promedio incorrecto: {promedio}")  # Output: 13.5 (incorrecto)

# ✅ Código correcto
promedio_correcto = sum(notas) / len(notas)
print(f"Promedio correcto: {promedio_correcto}")  # Output: 9.0

# -------------------------------------------------------------------
# 4️⃣ RESUMEN
# -------------------------------------------------------------------

# - SyntaxError: error de sintaxis, bloquea la ejecución
# - RuntimeError: error durante ejecución, depende de los datos o condiciones
# - LogicalError: el código funciona, pero los resultados son incorrectos

# Buenas prácticas:
# - Revisar sintaxis antes de ejecutar
# - Usar excepciones para manejar errores de runtime
# - Escribir tests para detectar errores lógicos
