# slicing_y_formateo.py
"""
Slicing y Formateo de Strings en Python – Nivel Profesional Backend

Este módulo cubre:
- Slicing de strings
- Formateo con f-strings y format()
- Métodos avanzados de strings
- Buenas prácticas profesionales
"""

# -------------------------------------------------
# 1. Indexación básica
# -------------------------------------------------
texto = "BackendPythonPro"
print(texto[0])    # 'B'
print(texto[-1])   # 'o'
print(texto[0:7])  # 'Backend'

# Indexación avanzada
print(texto[::2])  # 'BacePto' salto de 2
print(texto[::-1]) # invertir string 'orPyhPdnkcaB'

# -------------------------------------------------
# 2. Slicing profesional
# -------------------------------------------------
# Extraer subcadenas de forma clara
usuario = "juan.perez@example.com"
dominio = usuario.split("@")[1]  # 'example.com'
nombre = usuario.split("@")[0]   # 'juan.perez'

# Slicing para username
username = nombre[:4]  # 'juan'

# -------------------------------------------------
# 3. Formateo de strings
# -------------------------------------------------
edad = 25
ciudad = "Madrid"

# f-strings (Python 3.6+)
print(f"Usuario: {usuario}, Edad: {edad}, Ciudad: {ciudad}")

# format()
print("Usuario: {}, Edad: {}, Ciudad: {}".format(usuario, edad, ciudad))

# Concatenación clásica (no recomendado en backend profesional)
print("Usuario: " + usuario + ", Edad: " + str(edad))

# -------------------------------------------------
# 4. Métodos importantes de strings
# -------------------------------------------------
cadena = "   Python Profesional   "

# Limpieza
print(cadena.strip())   # 'Python Profesional'
print(cadena.lstrip())  # 'Python Profesional   '
print(cadena.rstrip())  # '   Python Profesional'

# Búsqueda
print(cadena.find("Pro"))  # 7
print(cadena.replace("Profesional", "Backend"))  # '   Python Backend   '

# Verificación
print(cadena.startswith("   Py"))  # True
print(cadena.endswith("onal   "))  # True
print(cadena.isalpha())             # False (espacios presentes)

# -------------------------------------------------
# 5. Slicing y formateo en backend
# -------------------------------------------------
# Ejemplo real: parseo de logs
log = "2025-12-18 12:34:56 | INFO | Usuario juan.perez creado"
fecha = log[:10]        # '2025-12-18'
hora = log[11:19]       # '12:34:56'
nivel = log[22:26]      # 'INFO'
mensaje = log[29:]      # 'Usuario juan.perez creado'

# Formateo para API o DB
registro = f"{fecha} {hora} | {nivel} | {mensaje}"
print(registro)

# -------------------------------------------------
# 6. Errores comunes de juniors
# -------------------------------------------------
# ❌ Olvidar índices negativos para slicing
# ❌ No usar strip() → strings con espacios
# ❌ Concatenación excesiva en lugar de f-strings
# ❌ No validar longitud de strings antes de slicing → IndexError
# ❌ No usar métodos built-in de Python → código largo y propenso a errores

# -------------------------------------------------
# 7. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Usar f-strings para claridad y eficiencia
# ✔️ Limpiar strings antes de procesar
# ✔️ Validar longitudes antes de slicing
# ✔️ Evitar concatenación innecesaria
# ✔️ Usar métodos built-in para búsqueda y reemplazo
# ✔️ Comentarios claros en transformaciones complejas

# -------------------------------------------------
# 8. Checklist mental backend
# -------------------------------------------------
# ✔️ Strings limpios y validados?  
# ✔️ Slicing seguro y legible?  
# ✔️ Formateo claro y profesional?  
# ✔️ Métodos built-in utilizados?  
# ✔️ Código fácil de mantener y escalar?

# -------------------------------------------------
# 9. Regla de oro
# -------------------------------------------------
"""
En backend profesional, tratar strings como un dato crítico: 
- Usa slicing seguro y claro
- Formatea con f-strings
- Limpia y valida cada string
- Evita concatenaciones y errores de índice

Esto hace tu código robusto, legible y profesional.
"""
