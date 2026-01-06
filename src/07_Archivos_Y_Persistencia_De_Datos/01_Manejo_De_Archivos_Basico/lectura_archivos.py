# lectura_archivos.py
# =======================
# Leer archivos en Python: read, readline, readlines
# Explicación paso a paso para comprender cómo funciona la lectura de archivos

# ---------------------------------------------------------
# 1️⃣ Abrir un archivo para lectura
# ---------------------------------------------------------
# Para leer un archivo primero debemos abrirlo en modo 'r' (read)
# Es muy recomendable especificar el encoding para evitar errores
archivo = open("ejemplo.txt", "r", encoding="utf-8")

# ---------------------------------------------------------
# 2️⃣ Leer todo el contenido con read()
# ---------------------------------------------------------
# `read()` lee TODO el contenido del archivo como una única cadena
contenido_completo = archivo.read()
print("Contenido completo:\n", contenido_completo)

# Consideraciones:
# - Muy útil para archivos pequeños
# - Si el archivo es muy grande, ocupará mucha memoria
# - Una vez leído, el cursor queda al final del archivo
#   -> Si volvemos a llamar `read()` devolverá una cadena vacía

# Reiniciamos el cursor al inicio para mostrar ejemplos posteriores
archivo.seek(0)  # Mueve el cursor al inicio

# ---------------------------------------------------------
# 3️⃣ Leer línea por línea con readline()
# ---------------------------------------------------------
# `readline()` lee **una línea a la vez**, incluyendo el salto de línea '\n'
linea1 = archivo.readline()
print("Primera línea:", linea1)

linea2 = archivo.readline()
print("Segunda línea:", linea2)

# Podemos usar un bucle para leer todo línea por línea
archivo.seek(0)  # Reiniciamos el cursor
print("\nLectura línea por línea:")
while True:
    linea = archivo.readline()
    if not linea:  # Cuando readline devuelve '', llegamos al final
        break
    print(linea.strip())  # .strip() elimina saltos de línea y espacios al inicio/final

# Ventajas:
# - Control total sobre cada línea
# - Útil cuando procesamos archivos muy grandes
# Desventajas:
# - Requiere bucle manual si queremos procesar todo el archivo

# ---------------------------------------------------------
# 4️⃣ Leer todas las líneas con readlines()
# ---------------------------------------------------------
# `readlines()` devuelve una lista con todas las líneas del archivo
archivo.seek(0)
todas_las_lineas = archivo.readlines()
print("\nLista de líneas:", todas_las_lineas)

# Podemos iterar fácilmente:
for linea in todas_las_lineas:
    print(linea.strip())

# Ventajas:
# - Conveniente para procesar todas las líneas como lista
# - Permite usar funciones de listas (map, filter, etc.)
# Desventajas:
# - Ocupa memoria proporcional al tamaño del archivo
# - Para archivos enormes puede ser ineficiente

# ---------------------------------------------------------
# 5️⃣ Buenas prácticas al leer archivos
# ---------------------------------------------------------
# 1. Siempre especificar encoding (utf-8 recomendado)
# 2. Cerrar archivos después de leer:
archivo.close()

# Alternativa profesional: context manager (`with`) que cierra automáticamente
with open("ejemplo.txt", "r", encoding="utf-8") as f:
    for linea in f:
        print("Con with:", linea.strip())

# 3. Elegir la estrategia de lectura según tamaño del archivo:
# - Archivos pequeños: read() o readlines()
# - Archivos grandes: readline() en bucle o iteración directa

# ---------------------------------------------------------
# ✅ Conclusión
# ---------------------------------------------------------
# Python ofrece varias formas de leer archivos:
# - read() → todo en una cadena
# - readline() → línea por línea
# - readlines() → todas las líneas en una lista
# Elegir correctamente depende de:
# - Tamaño del archivo
# - Operación que queremos realizar
# - Necesidad de eficiencia en memoria
