# lectura_escritura_archivos.py
"""
Lectura y Escritura de Archivos en Python – Nivel Profesional Backend

Este módulo cubre:
- Lectura y escritura de archivos de texto y binarios
- Uso de context managers
- Manejo de encoding
- Manejo de errores
- Buenas prácticas de backend
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

# -------------------------------------------------
# 1. Rutas y archivos
# -------------------------------------------------
# Usar pathlib en lugar de concatenar strings
ruta_archivo = Path("datos") / "usuarios.txt"

# Crear carpeta si no existe
ruta_archivo.parent.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# 2. Lectura de archivos de texto
# -------------------------------------------------
try:
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
        logging.info(f"Archivo leído correctamente, {len(contenido)} caracteres")
except FileNotFoundError:
    logging.error(f"Archivo no encontrado: {ruta_archivo}")
except Exception as e:
    logging.error(f"Error al leer archivo: {e}")


# -------------------------------------------------
# 3. Escritura de archivos de texto
# -------------------------------------------------
datos = "Usuario1, 25\nUsuario2, 30\n"
try:
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(datos)
        logging.info(f"Archivo escrito correctamente en {ruta_archivo}")
except Exception as e:
    logging.error(f"Error al escribir archivo: {e}")


# -------------------------------------------------
# 4. Lectura y escritura binaria
# -------------------------------------------------
binario = b"\x00\x01\x02"

ruta_bin = Path("datos") / "archivo.bin"

# Escritura
try:
    with open(ruta_bin, "wb") as f:
        f.write(binario)
        logging.info(f"Archivo binario escrito correctamente: {ruta_bin}")
except Exception as e:
    logging.error(f"Error al escribir archivo binario: {e}")

# Lectura
try:
    with open(ruta_bin, "rb") as f:
        contenido_bin = f.read()
        logging.info(f"Archivo binario leído correctamente, {len(contenido_bin)} bytes")
except Exception as e:
    logging.error(f"Error al leer archivo binario: {e}")


# -------------------------------------------------
# 5. Lectura línea a línea (para archivos grandes)
# -------------------------------------------------
try:
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            logging.info(f"Línea: {linea.strip()}")
except Exception as e:
    logging.error(f"Error al procesar archivo línea a línea: {e}")


# -------------------------------------------------
# 6. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Usar Pathlib para rutas
# ✔️ Context managers para abrir archivos
# ✔️ Manejar encoding explícitamente
# ✔️ Manejar excepciones específicas
# ✔️ Evitar hardcode de paths
# ✔️ Logging en vez de print
# ✔️ Evitar leer todo en memoria si el archivo es grande

# -------------------------------------------------
# 7. Errores comunes de juniors
# -------------------------------------------------
# ❌ Abrir archivos sin cerrar
# ❌ Ignorar excepciones
# ❌ Mezclar lectura binaria y texto sin control
# ❌ No validar existencia de carpetas
# ❌ Leer todo en memoria archivos enormes

# -------------------------------------------------
# 8. Checklist mental backend
# -------------------------------------------------
# ✔️ Rutas gestionadas correctamente?  
# ✔️ Archivos abiertos con with?  
# ✔️ Encoding explícito?  
# ✔️ Excepciones manejadas?  
# ✔️ Logging profesional?  
# ✔️ Código escalable y mantenible?

# -------------------------------------------------
# 9. Regla de oro
# -------------------------------------------------
"""
El manejo de archivos en backend profesional es un pilar:
- Usa Pathlib
- Context managers
- Logging
- Manejo de errores
- Evita cargar archivos enormes en memoria

Esto garantiza un backend robusto, seguro y profesional.
"""
