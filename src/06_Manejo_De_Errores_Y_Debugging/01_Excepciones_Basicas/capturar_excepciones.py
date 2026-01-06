"""
capturar_excepciones.py
=======================

Objetivo:
- Comprender la diferencia entre capturar excepciones específicas vs genéricas
- Aprender buenas prácticas para un manejo seguro y mantenible
"""

# -------------------------------------------------------------------
# 1️⃣ CAPTURA DE EXCEPCIONES ESPECÍFICAS
# -------------------------------------------------------------------

# ✅ Código limpio: captura solo los errores que se esperan
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error específico capturado: {e}")  # Output: division by zero
    resultado = 0

print(f"Resultado = {resultado}")

# Ventajas:
# - Se sabe exactamente qué error ocurrió
# - Evita ocultar errores inesperados
# - Facilita debug y logging preciso

# -------------------------------------------------------------------
# 2️⃣ CAPTURA DE EXCEPCIONES GENÉRICAS
# -------------------------------------------------------------------

# ❌ Mala práctica: captura cualquier excepción sin distinguir
try:
    resultado = 10 / 0
except Exception as e:
    print(f"Error genérico capturado: {e}")
    resultado = 0

print(f"Resultado = {resultado}")

# Riesgos:
# - Puede ocultar errores de programación (LogicalError, NameError)
# - Difícil de depurar
# - No sabemos si se manejó el error correcto o uno inesperado

# -------------------------------------------------------------------
# 3️⃣ CUANDO USAR EXCEPCIONES GENÉRICAS
# -------------------------------------------------------------------

# Solo en casos muy concretos y controlados:
# - Punto de entrada de la aplicación (main)
# - Para logging global antes de terminar
# - Nunca para lógica interna crítica

def main():
    try:
        # Código principal de la app
        x = int("abc")  # ValueError
    except Exception as e:
        # Log global de cualquier error inesperado
        print(f"Error inesperado en la aplicación: {e}")

main()

# -------------------------------------------------------------------
# 4️⃣ RESUMEN DE BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# 1. Captura siempre la excepción más específica posible
# 2. Evita except: o except Exception: salvo en puntos globales de logging
# 3. Documenta qué errores estás manejando y por qué
# 4. No uses try/except para controlar flujo normal de la aplicación
# 5. Siempre que captures, decide si vas a:
#    - Manejar el error
#    - Loguearlo
#    - Re-lanzarlo con raise si es crítico
