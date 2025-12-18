# errores_comunes_tipos.py
"""
Errores Comunes con Tipos de Datos en Python (Nivel Profesional)

Este módulo documenta:
- Errores de tipos MÁS FRECUENTES en backend real
- Por qué ocurren
- Cómo evitarlos de forma profesional
- Casos reales que rompen APIs y pipelines
"""

# -------------------------------------------------
# 1. Confiar en tipos sin validar (ERROR CRÍTICO)
# -------------------------------------------------

def calcular_iva(precio):
    return precio * 0.21

# ❌ Backend roto si llega string desde frontend
# calcular_iva("100") → '100100100100100100100100100'

# ✔️ Forma profesional
def calcular_iva_seguro(precio: float) -> float:
    if not isinstance(precio, (int, float)):
        raise TypeError("precio debe ser numérico")
    return precio * 0.21


# -------------------------------------------------
# 2. None no es 0, ni False, ni ""
# -------------------------------------------------

resultado = None

# ❌ Error común
# if resultado:
#     procesar(resultado)

# ✔️ Forma correcta
if resultado is not None:
    print("Hay resultado")

# None indica AUSENCIA de valor, no falsedad lógica


# -------------------------------------------------
# 3. Comparar floats directamente
# -------------------------------------------------

a = 0.1 + 0.2
b = 0.3

# ❌ Esto falla en producción
# if a == b:

# ✔️ Forma profesional
if abs(a - b) < 1e-9:
    print("Son iguales con tolerancia")


# -------------------------------------------------
# 4. Mezclar tipos en estructuras
# -------------------------------------------------

# ❌ Muy común en datos sucios
datos = [1, "2", 3, "cuatro"]

# Esto rompe cálculos
def sumar_datos(lista):
    total = 0
    for elemento in lista:
        total += elemento  # 💥 TypeError
    return total

# ✔️ Forma profesional
def sumar_datos_seguro(lista: list) -> int:
    total = 0
    for elemento in lista:
        try:
            total += int(elemento)
        except (ValueError, TypeError):
            continue
    return total


# -------------------------------------------------
# 5. Asumir que input() no falla
# -------------------------------------------------

# ❌
# edad = int(input("Edad: "))

# ✔️ Backend-safe
def pedir_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Valor inválido")


# -------------------------------------------------
# 6. Booleanos implícitos peligrosos
# -------------------------------------------------

# ❌ Error típico
estado = "False"

if estado:
    print("Usuario activo")  # ❌ Siempre entra

# ✔️ Forma correcta
estado = estado.lower() == "true"


# -------------------------------------------------
# 7. Mutabilidad mal entendida
# -------------------------------------------------

# ❌ Bug real de producción
def agregar_item(item, lista=[]):
    lista.append(item)
    return lista

# agregar_item(1) → [1]
# agregar_item(2) → [1, 2] ❌

# ✔️ Forma profesional
def agregar_item_seguro(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista


# -------------------------------------------------
# 8. Diccionarios con claves inconsistentes
# -------------------------------------------------

usuario = {
    "id": 1,
    "nombre": "Ana"
}

# ❌ KeyError en producción
# email = usuario["email"]

# ✔️ Forma segura
email = usuario.get("email")

if email is None:
    print("Usuario sin email")


# -------------------------------------------------
# 9. Tipos dinámicos ≠ caos
# -------------------------------------------------

# ❌ No tipar nada
def procesar(dato):
    return dato * 2

# ✔️ Tipado profesional
def procesar_seguro(dato: int | float) -> int | float:
    return dato * 2


# -------------------------------------------------
# 10. No lanzar errores cuando DEBES
# -------------------------------------------------

# ❌ Error silencioso
def dividir(a, b):
    if b == 0:
        return None
    return a / b

# ✔️ Forma profesional
def dividir_seguro(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("No se puede dividir entre 0")
    return a / b


# -------------------------------------------------
# 11. Checklist mental de supervivencia backend
# -------------------------------------------------
# ✔️ ¿Este dato viene de fuera? → VALIDAR
# ✔️ ¿Puede ser None? → COMPROBAR
# ✔️ ¿Puede fallar? → try/except
# ✔️ ¿Es float? → TOLERANCIA
# ✔️ ¿Es mutable? → CUIDADO
# ✔️ ¿Es crítico? → LANZAR ERROR
# ✔️ ¿Es confuso? → TIPAR
