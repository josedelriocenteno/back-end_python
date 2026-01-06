"""
fail_fast.py
============

Objetivo:
- Aprender el principio de fail-fast
- Detectar errores lo antes posible
- Evitar que fallos silenciosos se propaguen y compliquen el debugging
"""

# -------------------------------------------------------------------
# 1️⃣ QUÉ ES FAIL-FAST
# -------------------------------------------------------------------

# Fail-fast significa que tu aplicación detecta y reporta errores inmediatamente
# en lugar de continuar con datos corruptos o inconsistentes.

# Ventajas:
# 1. Menos efectos colaterales
# 2. Debugging más rápido
# 3. Código más seguro y predecible

# -------------------------------------------------------------------
# 2️⃣ EJEMPLO BÁSICO
# -------------------------------------------------------------------

def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero (fail-fast)")
    return a / b

# Uso
try:
    resultado = dividir(10, 0)
except ZeroDivisionError as e:
    print(f"Error detectado temprano: {e}")

# Aquí el programa falla rápido antes de hacer operaciones incorrectas

# -------------------------------------------------------------------
# 3️⃣ FAIL-FAST EN VALIDACIONES
# -------------------------------------------------------------------

def procesar_usuario(usuario: dict):
    # Validaciones fail-fast
    if "nombre" not in usuario or not usuario["nombre"]:
        raise ValueError("Nombre de usuario obligatorio")
    if "email" not in usuario or "@" not in usuario["email"]:
        raise ValueError("Email inválido")

usuario = {"nombre": "", "email": "correo.com"}

try:
    procesar_usuario(usuario)
except ValueError as e:
    print(f"Error detectado temprano: {e}")
    # Output: Nombre de usuario obligatorio

# -------------------------------------------------------------------
# 4️⃣ ANTI-PATTERN: FALLAR TARDE
# -------------------------------------------------------------------

# ❌ Mala práctica: validar tarde y propagar errores
def procesar_usuario_malo(usuario: dict):
    # Realiza muchas operaciones antes de validar
    print("Procesando datos...")
    print("Aplicando lógica de negocio...")
    # Ahora descubre el error
    if "nombre" not in usuario or not usuario["nombre"]:
        raise ValueError("Nombre de usuario obligatorio")  # demasiado tarde

# Problema: operaciones innecesarias ejecutadas antes de detectar error

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS FAIL-FAST
# -------------------------------------------------------------------

# 1. Validar inputs al inicio de funciones
# 2. Lanzar excepciones específicas inmediatamente cuando algo falla
# 3. Evitar procesar datos potencialmente corruptos
# 4. Usar fail-fast en testing: detectar bugs temprano
# 5. Combinar con logging para mantener trazabilidad de errores

# Resumen:
# - Detectar errores temprano = menos propagación
# - Código más predecible, mantenible y seguro
# - Facilita debugging y reduce costos de mantenimiento
