"""
raise_basico.py
===============

Objetivo:
- Aprender a lanzar excepciones de manera consciente
- Comprender cuándo interrumpir la ejecución por errores esperados
- Mantener código limpio y manejable
"""

# -------------------------------------------------------------------
# 1️⃣ LANZAR UNA EXCEPCIÓN BÁSICA
# -------------------------------------------------------------------

# Cuando detectamos un estado inválido en el programa
def dividir(a: float, b: float) -> float:
    """
    Divide a entre b.
    Lanza excepción si b es cero.
    """
    if b == 0:
        raise ZeroDivisionError("El denominador no puede ser cero")  # ❌ Consciente
    return a / b

# Uso
try:
    resultado = dividir(10, 0)
except ZeroDivisionError as e:
    print(f"Excepción capturada: {e}")  # Output: El denominador no puede ser cero

# -------------------------------------------------------------------
# 2️⃣ VALIDACIONES DE ENTRADAS
# -------------------------------------------------------------------

def crear_usuario(nombre: str, email: str):
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")
    if "@" not in email:
        raise ValueError("Email inválido")
    return {"nombre": nombre, "email": email}

# Uso
try:
    usuario = crear_usuario("", "correo.com")
except ValueError as e:
    print(f"Error de validación: {e}")  # Output: El nombre no puede estar vacío

# -------------------------------------------------------------------
# 3️⃣ CUANDO USAR RAISE
# -------------------------------------------------------------------

# 1. Cuando el estado o los argumentos son inválidos
# 2. Cuando no se puede continuar de manera segura
# 3. Para señalizar errores que deben ser manejados por el llamador
# 4. Para crear APIs claras y predecibles

# -------------------------------------------------------------------
# 4️⃣ RE-LANZAR EXCEPCIONES
# -------------------------------------------------------------------

# Se puede capturar y volver a lanzar para logging
def safe_dividir(a, b):
    try:
        return dividir(a, b)
    except ZeroDivisionError as e:
        print(f"Intento fallido de división: {e}")
        raise  # vuelve a lanzar la misma excepción

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# - Lanzar excepciones específicas, no genéricas Exception
# - Siempre documentar qué excepciones puede lanzar la función
# - Validar inputs antes de ejecutar lógica crítica
# - Usar raise para errores **esperados y manejables**, no para control de flujo normal
# - Combinar raise con logging cuando sea útil para debugging
