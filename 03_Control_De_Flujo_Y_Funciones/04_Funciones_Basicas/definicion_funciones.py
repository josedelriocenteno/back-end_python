# definicion_funciones.py
"""
FUNCIONES BÁSICAS EN PYTHON
===========================

Objetivo:
- Definir funciones limpias y reutilizables
- Comprender `def`, `return` y efectos secundarios
- Aplicable a backend, pipelines y preparación de datos
"""

# =========================================================
# 1. Definición básica de función
# =========================================================

def saludar(nombre):
    """Imprime un saludo personalizado (efecto secundario)"""
    print(f"Hola, {nombre}!")

saludar("Ana")  # Hola, Ana!

# =========================================================
# 2. Función con return
# =========================================================

def cuadrado(x):
    """Devuelve el cuadrado de un número (función pura)"""
    return x ** 2

resultado = cuadrado(5)
print(resultado)  # 25

# =========================================================
# 3. Función con múltiples parámetros
# =========================================================

def sumar(a, b):
    """Suma dos números"""
    return a + b

print(sumar(3, 7))  # 10

# =========================================================
# 4. Función con efecto secundario y return
# =========================================================

def registrar_usuario(nombre):
    """Registra usuario y devuelve mensaje"""
    print(f"Registrando usuario: {nombre}")  # efecto secundario
    return f"Usuario {nombre} registrado con éxito"

mensaje = registrar_usuario("Luis")
print(mensaje)

# =========================================================
# 5. Buenas prácticas
# =========================================================

# - Mantener funciones cortas y con responsabilidad única
# - Separar funciones puras de las que tienen efectos secundarios
# - Documentar con docstrings claros
# - Evitar modificar variables externas innecesariamente
# - Nombrar funciones de forma descriptiva y consistente
