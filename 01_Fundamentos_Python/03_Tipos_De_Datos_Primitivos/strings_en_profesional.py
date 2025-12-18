# strings_en_profesional.py
"""
Strings en Python Profesional

Este módulo cubre:
- Declaración y manipulación de strings
- Formateo y f-strings
- Métodos útiles
- Buenas prácticas profesionales
"""

# -------------------------------
# 1. Declaración de strings
# -------------------------------
# Comillas simples o dobles
mensaje1 = 'Hola mundo'
mensaje2 = "Hola mundo"

# Comillas triples para multilineas
mensaje_multilinea = """Este es un
mensaje
multilínea"""

# Strings vacíos
mensaje_vacio = ""

# -------------------------------
# 2. Indexado y slicing
# -------------------------------
texto = "Python Profesional"

# Acceder a caracteres
primer_caracter = texto[0]      # 'P'
ultimo_caracter = texto[-1]     # 'l'

# Substrings (slicing)
subtexto = texto[0:6]           # 'Python'
subtexto2 = texto[7:]           # 'Profesional'
subtexto3 = texto[:6]           # 'Python'
subtexto4 = texto[-10:-1]       # 'Profesiona'

# Paso en slicing
saltando_caracteres = texto[::2] # 'Pto roeional'

# -------------------------------
# 3. Operaciones con strings
# -------------------------------
# Concatenación
saludo = "Hola" + " " + "Mundo"   # 'Hola Mundo'

# Repetición
eco = "Hola! " * 3                # 'Hola! Hola! Hola! '

# Longitud
largo = len(texto)                 # 18

# Verificación
existe_python = "Python" in texto  # True
no_existe_java = "Java" not in texto  # True

# -------------------------------
# 4. Formateo de strings
# -------------------------------
nombre = "Juan"
edad = 25

# Concatenación clásica
mensaje = "Hola, mi nombre es " + nombre + " y tengo " + str(edad) + " años."

# Formato con format()
mensaje2 = "Hola, mi nombre es {} y tengo {} años.".format(nombre, edad)

# F-strings (Python 3.6+): recomendado profesional
mensaje3 = f"Hola, mi nombre es {nombre} y tengo {edad} años."

# Formateo avanzado
pi = 3.14159265
mensaje_pi = f"El valor de pi con 2 decimales: {pi:.2f}"  # '3.14'

# -------------------------------
# 5. Métodos útiles de strings
# -------------------------------
cadena = "  Python Profesional  "

# Limpieza
cadena_strip = cadena.strip()         # 'Python Profesional'

# Cambio de mayúsculas/minúsculas
cadena_upper = cadena.upper()         # '  PYTHON PROFESIONAL  '
cadena_lower = cadena.lower()         # '  python profesional  '
cadena_capitalize = cadena.capitalize() # '  python profesional  '
cadena_title = cadena.title()         # '  Python Profesional  '

# Reemplazo y búsqueda
cadena_reemplazada = cadena.replace("Python", "Java")  # '  Java Profesional  '
existe_palabra = "Profesional" in cadena               # True
posicion = cadena.find("Python")                       # 2

# Split y Join
palabras = cadena.strip().split()        # ['Python', 'Profesional']
frase = "-".join(palabras)              # 'Python-Profesional'

# -------------------------------
# 6. Buenas prácticas profesionales
# -------------------------------
# - Usar f-strings para claridad y rendimiento
# - Evitar concatenaciones excesivas
# - Usar métodos de strings en lugar de loops para eficiencia
# - Manejar None o cadenas vacías explícitamente
# - Documentar funciones que manipulen strings

def formatear_nombre_apellido(nombre: str, apellido: str) -> str:
    """
    Formatea un nombre y apellido con capitalización correcta.

    Args:
        nombre (str): Nombre del usuario
        apellido (str): Apellido del usuario

    Returns:
        str: Nombre completo capitalizado
    """
    return f"{nombre.strip().title()} {apellido.strip().title()}"

# Ejemplo de uso
nombre_completo = formatear_nombre_apellido(" juan", "pérez ")
print(nombre_completo)  # 'Juan Pérez'
