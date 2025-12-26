# excepciones_comunes.py
"""
Excepciones Comunes en Python – Backend Profesional

Este módulo cubre:
- Las excepciones más frecuentes en backend
- Cuándo y cómo capturarlas
- Patrones profesionales para manejarlas
- Errores típicos de juniors
"""

# -------------------------------------------------
# 1. ZeroDivisionError
# -------------------------------------------------
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: División por cero -> {e}")


# -------------------------------------------------
# 2. ValueError
# -------------------------------------------------
try:
    numero = int("abc")
except ValueError as e:
    print(f"Error: valor inválido -> {e}")


# -------------------------------------------------
# 3. TypeError
# -------------------------------------------------
try:
    suma = "2" + 2
except TypeError as e:
    print(f"Error: tipo incorrecto -> {e}")


# -------------------------------------------------
# 4. KeyError
# -------------------------------------------------
usuario = {"nombre": "Ana"}
try:
    print(usuario["edad"])
except KeyError as e:
    print(f"Error: clave inexistente -> {e}")


# -------------------------------------------------
# 5. IndexError
# -------------------------------------------------
lista = [1, 2, 3]
try:
    print(lista[5])
except IndexError as e:
    print(f"Error: índice fuera de rango -> {e}")


# -------------------------------------------------
# 6. AttributeError
# -------------------------------------------------
obj = None
try:
    obj.upper()
except AttributeError as e:
    print(f"Error: atributo inexistente -> {e}")


# -------------------------------------------------
# 7. FileNotFoundError
# -------------------------------------------------
try:
    with open("archivo_inexistente.txt") as f:
        contenido = f.read()
except FileNotFoundError as e:
    print(f"Error: archivo no encontrado -> {e}")


# -------------------------------------------------
# 8. ImportError / ModuleNotFoundError
# -------------------------------------------------
try:
    import modulo_que_no_existe
except ModuleNotFoundError as e:
    print(f"Error: módulo no encontrado -> {e}")


# -------------------------------------------------
# 9. Errores comunes de juniors
# -------------------------------------------------
# ❌ Capturar Exception genérico sin acción
# ❌ Ignorar el tipo de excepción y mezclar lógica
# ❌ No usar logging → difícil debug en producción
# ❌ No diferenciar KeyError vs AttributeError vs IndexError

# -------------------------------------------------
# 10. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Capturar excepciones específicas
# ✔️ Usar logging, no print, en producción
# ✔️ Bloques try cortos
# ✔️ Usar finally para cerrar recursos
# ✔️ Propagar si no puedes manejar
# ✔️ Documentar qué errores puede lanzar la función

# -------------------------------------------------
# 11. Checklist mental backend
# -------------------------------------------------
# ✔️ Sé qué excepciones pueden ocurrir?
# ✔️ Las estoy manejando correctamente?
# ✔️ Logging activado?
# ✔️ Recursos cerrados si aplica?
# ✔️ Código limpio y mantenible?

# -------------------------------------------------
# 12. Regla de oro
# -------------------------------------------------
"""
Conocer las excepciones más comunes y manejarlas correctamente
es la diferencia entre un backend estable y uno que falla en producción.
"""
