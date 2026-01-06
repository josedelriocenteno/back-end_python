"""
try_except_finally.py
=====================

Objetivo:
- Entender cómo usar try/except/finally correctamente
- Identificar malas prácticas en manejo de errores
- Aplicar patrones seguros y legibles
"""

# -------------------------------------------------------------------
# 1️⃣ USO BÁSICO DE TRY/EXCEPT
# -------------------------------------------------------------------

# Código sucio / mala práctica
# Captura genérica sin acción clara
try:
    x = 10 / 0
except:
    pass  # ❌ Error ignorado, difícil de debuggear

# ✅ Código limpio: captura específica y manejo adecuado
try:
    x = 10 / 0
except ZeroDivisionError as e:
    print(f"Error capturado: {e}")  # Output: division by zero
    x = 0  # Acción correctiva o valor por defecto

print(f"x = {x}")  # Output: x = 0

# -------------------------------------------------------------------
# 2️⃣ USO DE FINALLY
# -------------------------------------------------------------------

# finally se ejecuta siempre, haya o no excepción
# útil para liberar recursos, cerrar archivos, conexiones, etc.

# ❌ Mala práctica: no cerrar archivo si hay error
# f = open("archivo_inexistente.txt")
# contenido = f.read()  # Si falla, f nunca se cierra

# ✅ Buena práctica: usar finally
f = None
try:
    f = open("archivo_inexistente.txt", "r")
    contenido = f.read()
except FileNotFoundError as e:
    print(f"Error: {e}")
finally:
    if f:
        f.close()  # Siempre se ejecuta
        print("Archivo cerrado de forma segura")

# -------------------------------------------------------------------
# 3️⃣ TRY/EXCEPT/FINALLY CON FLUJO NORMAL
# -------------------------------------------------------------------

def dividir(a: float, b: float) -> float:
    """
    Divide a entre b de forma segura
    Args:
        a (float): numerador
        b (float): denominador
    Returns:
        float: resultado de la división, 0 si error
    """
    resultado = 0.0
    try:
        resultado = a / b
    except ZeroDivisionError as e:
        print(f"Error de división: {e}")
    finally:
        print(f"Intento de división {a}/{b} completado")
    return resultado

print(dividir(10, 2))  # Output: Intento completado, 5.0
print(dividir(10, 0))  # Output: Error capturado, Intento completado, 0.0

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS RESUMIDAS
# -------------------------------------------------------------------

# 1. Captura siempre excepciones específicas
# 2. Nunca dejar bloques except vacíos
# 3. Usar finally para liberar recursos críticos
# 4. Documentar la intención del try/except/finally
# 5. No usar try para controlar flujo normal del programa
