# with_archivos.py
# =====================
# Context manager aplicado a archivos en Python
# Uso profesional para abrir y cerrar archivos de forma segura

# ---------------------------------------------------------
# 1️⃣ Problema al abrir archivos "a la antigua"
# ---------------------------------------------------------
# Forma tradicional:
archivo = open("ejemplo.txt", "r", encoding="utf-8")
contenido = archivo.read()
archivo.close()  # Debemos recordar cerrar siempre

# Riesgos:
# - Si ocurre un error antes de `close()`, el archivo queda abierto
# - Esto puede causar fugas de memoria o bloqueos en sistemas concurrentes

# ---------------------------------------------------------
# 2️⃣ Introducción al context manager `with`
# ---------------------------------------------------------
# Python ofrece un patrón llamado *context manager*, que asegura:
# 1. Abrir el recurso al inicio del bloque
# 2. Cerrar el recurso automáticamente al terminar, incluso si ocurre un error

# Sintaxis:
# with open(ruta, modo, encoding) as variable:
#     hacer algo con variable

# ---------------------------------------------------------
# 3️⃣ Ejemplo básico de lectura con `with`
# ---------------------------------------------------------
with open("ejemplo.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
    print("Contenido leído con with:\n", contenido)

# Observaciones:
# - No necesitamos llamar `f.close()`
# - El archivo se cierra automáticamente al salir del bloque
# - Si ocurre un error dentro del bloque, igualmente se cierra

# ---------------------------------------------------------
# 4️⃣ Ejemplo de escritura con `with`
# ---------------------------------------------------------
lineas = ["Primera línea\n", "Segunda línea\n"]

with open("salida_with.txt", "w", encoding="utf-8") as f:
    f.writelines(lineas)

# Verificación
with open("salida_with.txt", "r", encoding="utf-8") as f:
    for linea in f:
        print("Leído:", linea.strip())

# ---------------------------------------------------------
# 5️⃣ Ventajas de `with` sobre open()/close()
# ---------------------------------------------------------
# ✅ Evita fugas de recursos y errores por no cerrar archivos
# ✅ Código más limpio y legible
# ✅ Compatible con cualquier objeto que implemente `__enter__` y `__exit__`
# ✅ Se integra con excepciones automáticamente

# ---------------------------------------------------------
# 6️⃣ Leer línea por línea con `with`
# ---------------------------------------------------------
with open("ejemplo.txt", "r", encoding="utf-8") as f:
    for linea in f:  # Iterar sobre el archivo devuelve cada línea
        print("Línea:", linea.strip())

# Ventaja sobre readline():
# - El bucle gestiona el cursor automáticamente
# - Muy eficiente incluso para archivos grandes
# - No carga todo en memoria como read() o readlines()

# ---------------------------------------------------------
# 7️⃣ Escribir múltiples líneas con `with`
# ---------------------------------------------------------
nombres = ["Ana\n", "Luis\n", "Marta\n"]
with open("nombres_with.txt", "w", encoding="utf-8") as f:
    f.writelines(nombres)

# ---------------------------------------------------------
# 8️⃣ Context manager y manejo de excepciones
# ---------------------------------------------------------
# Si ocurre un error dentro del bloque `with`, el archivo se cierra igualmente:
try:
    with open("ejemplo.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
        # Supongamos que hay un error de división
        x = 10 / 0
except ZeroDivisionError:
    print("Error capturado: división entre cero")
# El archivo ya está cerrado automáticamente al salir del bloque

# ---------------------------------------------------------
# ✅ Conclusión
# ---------------------------------------------------------
# Usar `with` es la forma profesional de trabajar con archivos en Python:
# - Garantiza cierre automático
# - Evita errores y fugas de memoria
# - Hace el código más legible y seguro
# - Puede combinarse con lectura, escritura, iteración y manejo de excepciones
