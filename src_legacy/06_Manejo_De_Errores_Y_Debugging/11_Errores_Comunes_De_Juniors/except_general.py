"""
except_general.py
==================

Objetivo:
- Mostrar por qué usar `except:` genérico es peligroso
- Enseñar cómo capturar excepciones específicas correctamente
- Evitar errores silenciosos y problemas de debugging en producción
"""

import logging

# -------------------------------------------------------------------
# 1️⃣ ANTI-PATRÓN: except: genérico
# -------------------------------------------------------------------

def leer_archivo_riesgoso(path):
    try:
        with open(path, "r") as f:
            contenido = f.read()
            return contenido
    except:
        # ❌ Anti-patrón: captura todo, incluyendo KeyboardInterrupt, SystemExit, MemoryError...
        logging.error("Ocurrió un error leyendo el archivo")
        return None

# Problema real:
# - No sabes qué tipo de error ocurrió
# - Podrías estar ocultando problemas graves
# - Debugging muy complicado

# -------------------------------------------------------------------
# 2️⃣ FORMA PROFESIONAL: captura específica
# -------------------------------------------------------------------

def leer_archivo_seguro(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logging.warning(f"Archivo no encontrado: {path}")
        return None
    except PermissionError:
        logging.error(f"No se tiene permiso para leer el archivo: {path}")
        return None
    except Exception as e:
        logging.critical(f"Error inesperado: {e}", exc_info=True)
        raise  # Re-lanzar para que no se oculte el fallo grave

# -------------------------------------------------------------------
# 3️⃣ EJECUCIÓN
# -------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    path_inexistente = "archivo_que_no_existe.txt"

    contenido_riesgoso = leer_archivo_riesgoso(path_inexistente)
    print("Contenido riesgoso:", contenido_riesgoso)

    contenido_seguro = leer_archivo_seguro(path_inexistente)
    print("Contenido seguro:", contenido_seguro)

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Evitar except: genérico → captura todo, incluso errores críticos
# 2️⃣ Capturar solo los errores que esperas y puedes manejar
# 3️⃣ Loggear siempre contexto completo para debugging
# 4️⃣ Re-lanzar excepciones inesperadas para evitar ocultar fallos graves
# 5️⃣ Mantener claridad en qué errores se manejan y cuáles no
# 6️⃣ Usar Exception solo como catch-all final, con logging crítico y raise
