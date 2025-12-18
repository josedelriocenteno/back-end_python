# int_float_bool_none.py
"""
Tipos de Datos Primitivos en Python: int, float, bool y None

Este módulo explica y ejemplifica los tipos de datos fundamentales de Python.
Se incluye:
- Declaración y uso de variables
- Operaciones básicas
- Buenas prácticas profesionales
"""

# -------------------------------
# 1. Enteros (int)
# -------------------------------
# Representan números enteros sin decimales
edad = 25
año_actual = 2025

# Operaciones básicas
suma = edad + 5          # 30
resta = año_actual - 2000 # 25
multiplicacion = edad * 2 # 50
division = año_actual / 2 # 1012.5 (resultado float)
division_entera = año_actual // 2 # 1012 (resultado int)
potencia = edad ** 2       # 625
modulo = año_actual % 4    # 1

# Conversión explícita
numero_str = "123"
numero_int = int(numero_str)  # Convierte str a int

# -------------------------------
# 2. Números de punto flotante (float)
# -------------------------------
altura = 1.75
peso = 70.5

# Operaciones
imc = peso / (altura ** 2)   # 23.02
suma_floats = altura + peso   # 72.25

# Conversión explícita
altura_int = int(altura)  # 1 (pierde decimales)

# Precisión: evitar comparaciones directas con floats
a = 0.1 + 0.2
b = 0.3
# if a == b: # Malo, puede fallar
if abs(a - b) < 1e-9:     # Pythonic y profesional
    print("Valores iguales dentro de tolerancia")

# -------------------------------
# 3. Booleanos (bool)
# -------------------------------
activo = True
inactivo = False

# Operaciones lógicas
logico_and = activo and inactivo  # False
logico_or = activo or inactivo    # True
logico_not = not activo           # False

# Booleanos en condicionales
if activo:
    print("Usuario activo")

# Conversión de otros tipos
bool(0)      # False
bool(1)      # True
bool("")     # False
bool("texto") # True

# -------------------------------
# 4. None
# -------------------------------
# Representa ausencia de valor o vacío
resultado = None

# Uso típico
def buscar_usuario(id_usuario):
    # Devuelve None si no encuentra usuario
    if id_usuario == 0:
        return None
    return {"id": id_usuario, "nombre": "Juan"}

usuario = buscar_usuario(0)
if usuario is None:
    print("Usuario no encontrado")

# -------------------------------
# 5. Buenas prácticas profesionales
# -------------------------------
# - Usar nombres claros: edad, altura, activo
# - Evitar hardcodear valores mágicos
# - Convertir tipos explícitamente cuando sea necesario
# - Evitar comparaciones directas con floats
# - Usar None para valores opcionales o vacíos
# - Tipado opcional para claridad y autocompletado

def calcular_imc(peso: float, altura: float) -> float:
    """
    Calcula el índice de masa corporal (IMC).

    Args:
        peso (float): Peso en kilogramos
        altura (float): Altura en metros

    Returns:
        float: IMC calculado
    """
    return peso / (altura ** 2)

# Ejemplo de uso
imc_juan = calcular_imc(peso=70.5, altura=1.75)
print(f"IMC de Juan: {imc_juan:.2f}")  # Formateo profesional
