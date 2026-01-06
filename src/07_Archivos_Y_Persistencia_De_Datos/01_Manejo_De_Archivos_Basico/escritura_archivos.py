# escritura_archivos.py
# =======================
# Escribir archivos en Python: write, writelines
# Explicación profunda y paso a paso, evitando asumir conocimientos previos

# ---------------------------------------------------------
# 1️⃣ Abrir un archivo para escribir
# ---------------------------------------------------------
# Para escribir usamos el modo 'w' (write), 'a' (append) o 'x' (exclusive)
# Siempre es recomendable especificar encoding="utf-8"

# 'w' → crea un archivo nuevo o sobrescribe uno existente
archivo = open("salida.txt", "w", encoding="utf-8")
print(type(archivo))  # <class '_io.TextIOWrapper'>

# ---------------------------------------------------------
# 2️⃣ Escribir con write()
# ---------------------------------------------------------
# El método `write()` recibe una cadena y la escribe en el archivo
archivo.write("Primera línea\n")  # No añade salto de línea automáticamente
archivo.write("Segunda línea\n")
archivo.close()  # Siempre cerrar para asegurar que se guarden los datos

# ---------------------------------------------------------
# 3️⃣ Escribir varias líneas con writelines()
# ---------------------------------------------------------
# `writelines()` recibe una lista (o iterable) de cadenas
# NO añade saltos de línea automáticamente, debemos incluirlos
lineas = ["Línea 1\n", "Línea 2\n", "Línea 3\n"]

archivo = open("salida.txt", "w", encoding="utf-8")
archivo.writelines(lineas)
archivo.close()

# ---------------------------------------------------------
# 4️⃣ Modos de apertura y sus efectos
# ---------------------------------------------------------
# 'w' → sobrescribe el archivo existente
# 'a' → añade al final, preservando contenido previo
# 'x' → crea archivo nuevo, falla si existe
# 'b' → para binario, útil si se serializa con pickle, imágenes, etc.

# Ejemplo: append
archivo = open("salida.txt", "a", encoding="utf-8")
archivo.write("Línea añadida al final\n")
archivo.close()

# ---------------------------------------------------------
# 5️⃣ Buenas prácticas de escritura
# ---------------------------------------------------------
# 1️⃣ Usar `with` para manejar cierre automático:
with open("salida_segura.txt", "w", encoding="utf-8") as f:
    f.write("Esta línea se guarda seguro\n")

# 2️⃣ Siempre especificar encoding para evitar errores de lectura posteriores
# 3️⃣ Incluir saltos de línea '\n' al escribir varias líneas
# 4️⃣ Elegir modo correcto según el comportamiento deseado:
# - 'w' para sobrescribir
# - 'a' para añadir
# - 'x' para crear solo si no existe

# ---------------------------------------------------------
# 6️⃣ Errores comunes al escribir
# ---------------------------------------------------------
# ❌ Olvidar cerrar el archivo → pérdida de datos o corrupción
# ❌ No poner '\n' → todas las líneas se concatenan
# ❌ Usar 'w' por error → se borran datos existentes
# ❌ No especificar encoding → errores de lectura en otros sistemas

# ---------------------------------------------------------
# 7️⃣ Ejemplo completo: escribir y leer
# ---------------------------------------------------------
# Escribir con 'writelines' y luego leer con 'readlines'
lineas_para_guardar = ["Juan\n", "Ana\n", "Luis\n"]

# Escribir
with open("nombres.txt", "w", encoding="utf-8") as f:
    f.writelines(lineas_para_guardar)

# Leer para comprobar
with open("nombres.txt", "r", encoding="utf-8") as f:
    contenido = f.readlines()
    print("Contenido guardado:", [linea.strip() for linea in contenido])

# ---------------------------------------------------------
# ✅ Conclusión
# ---------------------------------------------------------
# - `write()` → línea individual o cadena grande
# - `writelines()` → múltiples líneas desde lista/iterable
# - Modos 'w', 'a', 'x' definen comportamiento sobre archivos existentes
# - Siempre usar encoding y cerrar archivos, preferiblemente con `with`
# - Controlar cuidadosamente los saltos de línea para que los datos sean legibles
