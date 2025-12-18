# conversiones_y_casting.py
"""
Conversiones y Casting en Python Profesional

Este módulo cubre:
- Qué es el casting y cuándo usarlo
- Conversiones entre tipos primitivos
- Conversión segura de datos externos (input, APIs, archivos)
- Errores comunes y cómo evitarlos
- Buenas prácticas profesionales en backend y data
"""

# -------------------------------------------------
# 1. Qué es casting
# -------------------------------------------------
# Casting = conversión explícita de un tipo de dato a otro
# Python NO convierte automáticamente entre tipos incompatibles

numero_str = "100"
numero_int = int(numero_str)     # str -> int
numero_float = float(numero_str) # str -> float

# -------------------------------------------------
# 2. Conversiones básicas entre tipos
# -------------------------------------------------

# int -> float
edad = 25
edad_float = float(edad)  # 25.0

# float -> int (TRUNCA, no redondea)
precio = 19.99
precio_int = int(precio)  # 19 ⚠️

# int / float -> str
cantidad = 3
cantidad_str = str(cantidad)

# bool -> int
True_as_int = int(True)   # 1
False_as_int = int(False) # 0

# int -> bool
bool_0 = bool(0)   # False
bool_1 = bool(1)   # True
bool_100 = bool(100)  # True

# -------------------------------------------------
# 3. Conversión de strings
# -------------------------------------------------

# Strings válidos
numero_ok = "42"
print(int(numero_ok))     # 42

decimal_ok = "3.14"
print(float(decimal_ok))  # 3.14

# Strings NO válidos → ValueError
numero_error = "42a"

# int(numero_error)  # ❌ ValueError

# Conversión segura
def convertir_a_int(valor: str) -> int | None:
    """
    Convierte un string a int de forma segura.

    Args:
        valor (str): valor a convertir

    Returns:
        int | None: entero convertido o None si falla
    """
    try:
        return int(valor)
    except ValueError:
        return None

resultado = convertir_a_int("123")
resultado_error = convertir_a_int("123x")

# -------------------------------------------------
# 4. Casting en input del usuario (MUY IMPORTANTE)
# -------------------------------------------------

# input() SIEMPRE devuelve str
# edad = input("Introduce tu edad: ")
# edad + 1  ❌ TypeError

# Forma correcta
# edad = int(input("Introduce tu edad: "))
# edad + 1  ✔️

# Forma profesional y segura
def pedir_edad() -> int:
    while True:
        entrada = input("Introduce tu edad: ")
        try:
            return int(entrada)
        except ValueError:
            print("Edad inválida, introduce un número.")

# -------------------------------------------------
# 5. Casting en datos externos (APIs, JSON, archivos)
# -------------------------------------------------

# Simulación de datos externos (JSON)
datos_api = {
    "id": "10",
    "activo": "true",
    "saldo": "250.75"
}

user_id = int(datos_api["id"])
saldo = float(datos_api["saldo"])

# Conversión manual de booleanos desde strings
activo = datos_api["activo"].lower() == "true"

# -------------------------------------------------
# 6. None y casting
# -------------------------------------------------

valor = None

# int(valor)  ❌ TypeError

# Forma profesional
if valor is not None:
    valor_int = int(valor)

# -------------------------------------------------
# 7. Errores comunes (MUY IMPORTANTES)
# -------------------------------------------------

# ❌ Asumir que Python convierte solo
# "10" + 5 → TypeError

# ❌ Convertir sin validar datos externos
# int("abc") → ValueError

# ❌ Usar int() para redondear
# int(9.9) → 9 (NO redondea)

# ✔️ Usar round()
redondeado = round(9.9)  # 10

# -------------------------------------------------
# 8. Buenas prácticas profesionales
# -------------------------------------------------
# - Convertir datos lo antes posible (input, APIs)
# - Validar SIEMPRE datos externos
# - No asumir formatos correctos
# - Usar funciones auxiliares para casting seguro
# - Documentar conversiones críticas
# - No ocultar errores silenciosamente

def convertir_precio(valor: str) -> float:
    """
    Convierte un precio a float validando el formato.

    Args:
        valor (str): precio en formato string

    Returns:
        float: precio convertido

    Raises:
        ValueError: si el formato es inválido
    """
    try:
        return float(valor)
    except ValueError as e:
        raise ValueError(f"Precio inválido: {valor}") from e

# -------------------------------------------------
# 9. Checklist mental (backend real)
# -------------------------------------------------
# ✔️ ¿Este dato viene de fuera? → VALIDAR
# ✔️ ¿Estoy seguro del tipo? → CASTING EXPLÍCITO
# ✔️ ¿Puede ser None? → COMPROBAR
# ✔️ ¿Puede fallar? → try/except
# ✔️ ¿Es crítico? → documentar y testear
