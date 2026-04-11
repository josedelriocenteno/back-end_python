# metodos_importantes_strings.py
"""
Métodos Importantes de Strings en Python – Backend Profesional

Este módulo cubre:
- Métodos built-in esenciales para strings
- Transformaciones, búsqueda, limpieza y validación
- Buenas prácticas para backend y procesamiento de datos
"""

# -------------------------------------------------
# 1. Limpieza de strings
# -------------------------------------------------
cadena = "   Hola Backend Python   "

print(cadena.strip())   # 'Hola Backend Python' (elimina espacios al inicio y fin)
print(cadena.lstrip())  # 'Hola Backend Python   ' (elimina solo al inicio)
print(cadena.rstrip())  # '   Hola Backend Python' (elimina solo al final)

# -------------------------------------------------
# 2. Transformación de case
# -------------------------------------------------
texto = "python professional"
print(texto.upper())   # 'PYTHON PROFESSIONAL'
print(texto.lower())   # 'python professional'
print(texto.title())   # 'Python Professional'
print(texto.capitalize())  # 'Python professional'

# -------------------------------------------------
# 3. Búsqueda y reemplazo
# -------------------------------------------------
frase = "Error en el servidor: código 500"

print(frase.find("servidor"))  # 9 (primer índice de aparición)
print(frase.replace("500", "200"))  # 'Error en el servidor: código 200'
print("Error" in frase)  # True

# -------------------------------------------------
# 4. División y unión
# -------------------------------------------------
usuarios = "juan,pedro,maria"
lista_usuarios = usuarios.split(",")  # ['juan', 'pedro', 'maria']
print(lista_usuarios)

# Unión
cadena_usuarios = "-".join(lista_usuarios)
print(cadena_usuarios)  # 'juan-pedro-maria'

# -------------------------------------------------
# 5. Validación y verificación
# -------------------------------------------------
print("123".isdigit())    # True
print("abc".isalpha())    # True
print("abc123".isalnum()) # True
print(" ".isspace())      # True

# -------------------------------------------------
# 6. Padding y alineación
# -------------------------------------------------
usuario = "Juan"
print(usuario.rjust(10))  # '      Juan'  # derecha
print(usuario.ljust(10))  # 'Juan      '  # izquierda
print(usuario.center(10)) # '   Juan   '  # centro

# -------------------------------------------------
# 7. Ejemplo profesional en backend
# -------------------------------------------------
log = "2025-12-18 12:34:56 | INFO | Usuario juan.perez creado"
# Extraer fecha, hora, nivel y mensaje
fecha = log[:10]
hora = log[11:19]
nivel = log[22:26]
mensaje = log[29:]

# Limpiar y formatear para DB o API
mensaje = mensaje.strip()
registro = f"{fecha} {hora} | {nivel} | {mensaje}"
print(registro)

# -------------------------------------------------
# 8. Errores comunes de juniors
# -------------------------------------------------
# ❌ No usar strip() → strings con espacios basura
# ❌ Usar concatenación en vez de join() → ineficiente
# ❌ Ignorar validación de caracteres → errores en datos
# ❌ Mezclar mayúsculas/minúsculas sin control
# ❌ No usar métodos built-in → código largo y propenso a errores

# -------------------------------------------------
# 9. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Siempre limpiar strings antes de procesar
# ✔️ Usar join/split para concatenación/división
# ✔️ Validar contenido antes de usar
# ✔️ Aprovechar métodos built-in para eficiencia
# ✔️ Comentarios claros para transformaciones complejas
# ✔️ Usar f-strings para formateo final

# -------------------------------------------------
# 10. Checklist mental backend
# -------------------------------------------------
# ✔️ Strings limpios y validados?  
# ✔️ Métodos built-in aprovechados?  
# ✔️ Transformaciones claras y seguras?  
# ✔️ Código legible, mantenible y escalable?

# -------------------------------------------------
# 11. Regla de oro
# -------------------------------------------------
"""
Domina los métodos de strings y tu backend podrá procesar, validar y transformar datos
de manera robusta, profesional y eficiente desde el día 1.
"""
