"""
jerarquia_excepciones.py
========================

Objetivo:
- Diseñar jerarquías de excepciones limpias y escalables
- Mejorar manejo de errores en proyectos grandes
- Permitir captura específica o general según necesidad
"""

# -------------------------------------------------------------------
# 1️⃣ PRINCIPIOS DE DISEÑO DE JERARQUÍA
# -------------------------------------------------------------------

# 1. Tener una excepción base por dominio
# 2. Extenderla para subcategorías de errores
# 3. Mantener consistencia en nombres y mensajes
# 4. Facilitar captura agrupada o específica

# -------------------------------------------------------------------
# 2️⃣ EJEMPLO DE JERARQUÍA DE EXCEPCIONES
# -------------------------------------------------------------------

# Excepción base para toda la aplicación
class AppError(Exception):
    """Excepción base de la aplicación"""
    pass

# Subcategorías
class UsuarioError(AppError):
    """Errores relacionados con usuarios"""
    pass

class ProductoError(AppError):
    """Errores relacionados con productos"""
    pass

class PedidoError(AppError):
    """Errores relacionados con pedidos"""
    pass

# Sub-subcategorías para mayor granularidad
class UsuarioInvalidoError(UsuarioError):
    """Usuario con datos inválidos"""
    pass

class UsuarioNoEncontradoError(UsuarioError):
    """Usuario no existe en base de datos"""
    pass

class ProductoInvalidoError(ProductoError):
    """Producto con precio o nombre inválido"""
    pass

# -------------------------------------------------------------------
# 3️⃣ USO PRÁCTICO DE LA JERARQUÍA
# -------------------------------------------------------------------

# Función que lanza excepción específica
def buscar_usuario(usuario_id: int):
    if usuario_id != 1:
        raise UsuarioNoEncontradoError(f"Usuario con id {usuario_id} no encontrado")

try:
    buscar_usuario(2)
except UsuarioNoEncontradoError as e:
    print(f"Error específico: {e}")  # Output: Usuario con id 2 no encontrado
except UsuarioError as e:
    print(f"Error general de usuario: {e}")
except AppError as e:
    print(f"Error de aplicación: {e}")

# -------------------------------------------------------------------
# 4️⃣ VENTAJAS DE UNA JERARQUÍA BIEN DISEÑADA
# -------------------------------------------------------------------

# 1. Captura flexible:
#    - Podemos capturar errores muy específicos o generales según contexto
# 2. Código más legible:
#    - Cada error tiene un significado claro
# 3. Escalabilidad:
#    - Fácil de extender cuando el proyecto crece
# 4. Debugging más sencillo:
#    - Logs claros, jerarquía explícita

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# - Siempre crear una excepción base para cada dominio de tu app
# - Heredar de esa base para errores específicos
# - Evitar lanzar Exception genérica
# - Documentar qué errores puede lanzar cada función
# - Usar nombres descriptivos: <Dominio><TipoError>, por ejemplo:
#   UsuarioInvalidoError, PedidoNoEncontradoError
