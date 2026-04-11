# abrir_cerrar_archivos.py
# =========================
# Cómo abrir y cerrar archivos en Python de forma correcta
# Incluye explicación de modos, encoding y buenas prácticas

# ---------------------------------------------------------
# 1️⃣ Abrir un archivo
# ---------------------------------------------------------
# Para trabajar con archivos en Python se usa la función integrada `open()`.
# Sintaxis básica:
# open(ruta_archivo, modo, encoding=None)
#
# Parámetros:
# - ruta_archivo: la ruta al archivo (puede ser relativa o absoluta)
# - modo: cómo vamos a usar el archivo ('r', 'w', 'a', 'x', etc.)
# - encoding: codificación de caracteres (muy importante para textos)

# Ejemplo mínimo: abrir un archivo en modo lectura
archivo = open("ejemplo.txt", "r")  # 'r' = read (lectura)
# Esto devuelve un objeto de tipo _io.TextIOWrapper
print(type(archivo))  # <class '_io.TextIOWrapper'>

# ---------------------------------------------------------
# 2️⃣ Modos de apertura de archivos
# ---------------------------------------------------------
# Modo | Descripción
# 'r'  | Solo lectura. Error si el archivo no existe.
# 'w'  | Escritura. Crea el archivo si no existe, o lo trunca si existe.
# 'a'  | Append (agregar). Añade contenido al final sin borrar lo existente.
# 'x'  | Exclusivo. Crea un archivo nuevo, error si ya existe.
# 'b'  | Binary. Para datos binarios, como imágenes o pickle.
# '+'  | Actualización: lectura y escritura simultánea.

# Ejemplo: abrir en modo escritura
archivo = open("ejemplo2.txt", "w", encoding="utf-8")  # 'w' + UTF-8
archivo.write("Hola mundo\n")
archivo.write("Segunda línea\n")
archivo.close()  # ¡Muy importante cerrar el archivo!

# ---------------------------------------------------------
# 3️⃣ Importancia de cerrar archivos
# ---------------------------------------------------------
# Siempre debemos cerrar el archivo con `.close()` para:
# - Liberar recursos del sistema
# - Asegurar que los datos se escriban en disco (flush)
# - Evitar errores de bloqueo de archivo en sistemas concurrentes

# Ejemplo incorrecto (anti-patrón):
archivo = open("ejemplo.txt", "r")
contenido = archivo.read()
# Oops, olvidamos cerrar → riesgo de fuga de recursos

# ---------------------------------------------------------
# 4️⃣ Manejo de encoding
# ---------------------------------------------------------
# El encoding define cómo se interpretan los caracteres.
# Por defecto, Python puede usar la codificación del sistema (Windows: cp1252, Linux: utf-8)
# Para portabilidad y evitar errores, siempre es recomendable usar utf-8.

# Ejemplo seguro:
with open("ejemplo_utf8.txt", "w", encoding="utf-8") as f:
    f.write("Texto con acentos: áéíóú ñ ü")

# Si abres sin el encoding correcto, puede fallar al leer:
# UnicodeDecodeError: 'cp1252' codec can't decode byte ...

# ---------------------------------------------------------
# 5️⃣ Buenas prácticas iniciales
# ---------------------------------------------------------
# ✅ Siempre cerrar archivos, preferiblemente con `with` (context manager)
# ✅ Especificar `encoding="utf-8"` para texto
# ✅ Elegir el modo correcto según la operación
# ✅ Evitar sobrescribir archivos sin querer ('w' trunca, usar 'a' o 'x' si no quieres perder datos)
# ✅ Manejar posibles errores con try/except (lo veremos en detalle más adelante)

# ---------------------------------------------------------
# 6️⃣ Resumen práctico
# ---------------------------------------------------------
# Leer archivo
archivo = open("ejemplo.txt", "r", encoding="utf-8")
contenido = archivo.read()
archivo.close()

# Escribir archivo (sobrescribiendo)
archivo = open("ejemplo.txt", "w", encoding="utf-8")
archivo.write("Nueva línea\n")
archivo.close()

# Agregar al final
archivo = open("ejemplo.txt", "a", encoding="utf-8")
archivo.write("Otra línea añadida\n")
archivo.close()

# ---------------------------------------------------------
# ✅ Conclusión
# ---------------------------------------------------------
# Abrir y cerrar archivos puede parecer trivial, pero es **fundamental hacerlo bien**:
# - Evitar pérdidas de datos
# - Evitar fugas de recursos
# - Garantizar compatibilidad y portabilidad
# La próxima lección enseñará a **usar context managers (`with`)** para automatizar el cierre seguro.
