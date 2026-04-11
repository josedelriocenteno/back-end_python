"""
excepciones_personalizadas.py
=============================

Objetivo:
- Aprender a crear clases de excepción propias
- Mejorar claridad y control de errores en aplicaciones complejas
- Integrar excepciones personalizadas en flujo de control
"""

# -------------------------------------------------------------------
# 1️⃣ CREACIÓN BÁSICA DE UNA EXCEPCIÓN PERSONALIZADA
# -------------------------------------------------------------------

# Heredamos de Exception o de una subclase apropiada
class ErrorUsuario(Exception):
    """Excepción personalizada para errores relacionados con usuarios"""
    pass

class ErrorProducto(Exception):
    """Excepción para errores en la gestión de productos"""
    pass

# -------------------------------------------------------------------
# 2️⃣ USO EN FUNCIONES
# -------------------------------------------------------------------

def crear_usuario(nombre: str, email: str):
    if not nombre:
        raise ErrorUsuario("El nombre del usuario no puede estar vacío")
    if "@" not in email:
        raise ErrorUsuario("Email inválido")
    return {"nombre": nombre, "email": email}

def agregar_producto(nombre: str, precio: float):
    if precio < 0:
        raise ErrorProducto("El precio no puede ser negativo")
    return {"nombre": nombre, "precio": precio}

# -------------------------------------------------------------------
# 3️⃣ CAPTURA DE EXCEPCIONES PERSONALIZADAS
# -------------------------------------------------------------------

try:
    usuario = crear_usuario("", "correo.com")
except ErrorUsuario as e:
    print(f"Error de usuario: {e}")  # Output: El nombre del usuario no puede estar vacío

try:
    producto = agregar_producto("Camiseta", -10)
except ErrorProducto as e:
    print(f"Error de producto: {e}")  # Output: El precio no puede ser negativo

# -------------------------------------------------------------------
# 4️⃣ JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# -------------------------------------------------------------------

# Podemos crear jerarquías para agrupar errores
class ErrorApp(Exception):
    """Error base de la aplicación"""
    pass

class ErrorDB(ErrorApp):
    """Errores relacionados con la base de datos"""
    pass

class ErrorValidacion(ErrorApp):
    """Errores de validación de datos"""
    pass

# Uso práctico
def conectar_db(url: str):
    if not url.startswith("db://"):
        raise ErrorDB("URL de base de datos inválida")

try:
    conectar_db("localhost")
except ErrorApp as e:
    print(f"Error general de la app: {e}")  # Captura todos los errores derivados de ErrorApp

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# 1. Crear excepción específica para cada dominio lógico de tu app
# 2. Heredar siempre de Exception o de otra excepción personalizada
# 3. Documentar qué funciones lanzan cada tipo de excepción
# 4. Usar jerarquías para poder capturar errores de forma agrupada si es necesario
# 5. No usar excepciones personalizadas para flujo normal, solo para **situaciones excepcionales**
