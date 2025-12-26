# try_except_else_finally.py
"""
Manejo Profesional de Excepciones en Python – Nivel Backend

Este módulo cubre:
- Uso de try, except, else y finally
- Patrones de manejo de errores en producción
- Cómo evitar crashes silenciosos
- Errores comunes de juniors
"""

# -------------------------------------------------
# 1. Estructura básica
# -------------------------------------------------

try:
    resultado = 10 / 2
except ZeroDivisionError as e:
    print(f"Error: {e}")
else:
    print(f"Operación exitosa, resultado: {resultado}")
finally:
    print("Bloque finally siempre se ejecuta")


# -------------------------------------------------
# 2. Uso profesional de except
# -------------------------------------------------

# ❌ Capturar Exception genérico
# try:
#     ...
# except Exception:
#     pass  # oculta errores → muy peligroso

# ✔️ Capturar errores específicos
try:
    x = int("abc")
except ValueError as e:
    print(f"Valor inválido: {e}")

# ✔️ Logging en producción
import logging
logging.basicConfig(level=logging.INFO)
try:
    x = int("abc")
except ValueError as e:
    logging.error(f"Error de conversión: {e}")


# -------------------------------------------------
# 3. Bloque else
# -------------------------------------------------

# Se ejecuta solo si NO hubo excepción
try:
    y = 10 / 2
except ZeroDivisionError:
    print("División por cero")
else:
    logging.info(f"Resultado correcto: {y}")


# -------------------------------------------------
# 4. Bloque finally
# -------------------------------------------------

# Siempre se ejecuta, útil para cerrar recursos
file = None
try:
    file = open("archivo.txt", "r")
    contenido = file.read()
except FileNotFoundError as e:
    logging.error(f"No se encontró el archivo: {e}")
finally:
    if file:
        file.close()


# -------------------------------------------------
# 5. Manejo de múltiples excepciones
# -------------------------------------------------

try:
    valor = int("abc")
    resultado = 10 / valor
except (ValueError, ZeroDivisionError) as e:
    logging.error(f"Ocurrió un error: {e}")


# -------------------------------------------------
# 6. Propagar errores (raise)
# -------------------------------------------------

def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b

try:
    dividir(10, 0)
except ValueError as e:
    logging.warning(f"Advertencia: {e}")


# -------------------------------------------------
# 7. Errores comunes de juniors
# -------------------------------------------------
# ❌ Capturar Exception sin acción
# ❌ Silenciar errores con pass
# ❌ Usar try en demasiadas líneas → difícil mantenimiento
# ❌ Ignorar finally → fugas de recursos

# -------------------------------------------------
# 8. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Capturar excepciones específicas
# ✔️ Usar logging, no print
# ✔️ Bloques try cortos, claros
# ✔️ Usar else para código seguro
# ✔️ finally para cerrar recursos
# ✔️ Propagar errores si no puedes manejar

# -------------------------------------------------
# 9. Checklist mental backend
# -------------------------------------------------
# ✔️ Sé qué excepción puede ocurrir?
# ✔️ La estoy capturando correctamente?
# ✔️ Logging o alertas activadas?
# ✔️ Recursos cerrados en finally?
# ✔️ Código limpio y mantenible?

# -------------------------------------------------
# 10. Regla de oro
# -------------------------------------------------
"""
Gestionar errores no es opcional: es lo que mantiene tu backend vivo
y confiable en producción.
"""
