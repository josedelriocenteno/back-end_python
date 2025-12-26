# input_y_output_basico.py
"""
Input y Output Básico en Python – Nivel Profesional Backend

Este módulo cubre:
- Lectura de datos desde consola y archivos
- Escritura de datos
- Validación y sanitización de inputs
- Errores comunes y buenas prácticas
"""

# -------------------------------------------------
# 1. Entrada desde consola
# -------------------------------------------------
# input() devuelve siempre str
nombre = input("Introduce tu nombre: ")
print(f"Hola, {nombre}")

# Validación mínima profesional
while True:
    edad_str = input("Introduce tu edad: ")
    try:
        edad = int(edad_str)
        if edad < 0:
            raise ValueError("Edad no puede ser negativa")
        break
    except ValueError as e:
        print(f"Entrada inválida: {e}, intenta de nuevo")

print(f"Edad validada: {edad}")


# -------------------------------------------------
# 2. Salida profesional
# -------------------------------------------------
# Print para debugging
print(f"Usuario: {nombre}, Edad: {edad}")

# Logging profesional
import logging
logging.basicConfig(level=logging.INFO)
logging.info(f"Usuario registrado: {nombre}, Edad: {edad}")


# -------------------------------------------------
# 3. Lectura de archivos
# -------------------------------------------------
# Abrir y leer contenido
try:
    with open("datos.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
        logging.info(f"Archivo leído correctamente, {len(contenido)} caracteres")
except FileNotFoundError:
    logging.error("Archivo datos.txt no encontrado")
except Exception as e:
    logging.error(f"Error inesperado al leer archivo: {e}")


# -------------------------------------------------
# 4. Escritura de archivos
# -------------------------------------------------
try:
    with open("salida.txt", "w", encoding="utf-8") as f:
        f.write(f"Usuario: {nombre}, Edad: {edad}\n")
        logging.info("Archivo salida.txt escrito correctamente")
except Exception as e:
    logging.error(f"Error al escribir archivo: {e}")


# -------------------------------------------------
# 5. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Siempre cerrar archivos (con with)
# ✔️ Manejar excepciones
# ✔️ Validar y sanitizar inputs
# ✔️ Usar logging en lugar de print en producción
# ✔️ Evitar hardcode de paths, usar variables de entorno o pathlib


# -------------------------------------------------
# 6. Errores comunes de juniors
# -------------------------------------------------
# ❌ No validar inputs
# ❌ Ignorar excepciones al leer/escribir archivos
# ❌ Mezclar print y logging en producción
# ❌ Usar encoding por defecto sin control
# ❌ Abrir archivos sin context manager → fugas de recursos


# -------------------------------------------------
# 7. Checklist mental backend
# -------------------------------------------------
# ✔️ Inputs validados y sanitizados?  
# ✔️ Archivos manejados correctamente?  
# ✔️ Logging en lugar de print para producción?  
# ✔️ Recursos cerrados automáticamente?  
# ✔️ Código limpio y mantenible?


# -------------------------------------------------
# 8. Regla de oro
# -------------------------------------------------
"""
Trata la entrada y salida como **primer punto de defensa y calidad**:
- Valida todo lo que recibes
- Maneja excepciones correctamente
- Logging en lugar de print
- Archivos cerrados siempre
Esto garantiza que tu backend sea profesional y robusto desde el día 1.
"""
