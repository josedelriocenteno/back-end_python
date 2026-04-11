# docstrings.py
"""
DOCUMENTACIÓN PROFESIONAL EN PYTHON
==================================

Objetivo:
- Aprender a documentar funciones, clases y módulos correctamente
- Mejorar la legibilidad y mantenibilidad del código
- Facilitar la colaboración en proyectos backend, APIs y pipelines de datos

Contexto:
- Los docstrings son cadenas de texto que van al inicio de funciones, clases o módulos
- Permiten que herramientas automáticas (IDE, Sphinx, linters) generen documentación
- Clave en proyectos profesionales para estandarizar la información sobre el código
"""

# =========================================================
# 1. Docstrings básicos en funciones
# =========================================================

def sumar(a: int, b: int) -> int:
    """
    Suma dos números enteros.

    Parámetros:
    ----------
    a : int
        Primer número a sumar.
    b : int
        Segundo número a sumar.

    Retorna:
    -------
    int
        Resultado de la suma de a + b.

    Ejemplo:
    -------
    >>> sumar(3, 5)
    8
    """
    return a + b

# =========================================================
# 2. Docstrings en funciones con *args y **kwargs
# =========================================================

def crear_usuario(nombre: str, *args, rol: str = "usuario", **kwargs):
    """
    Crea un usuario con información flexible.

    Parámetros:
    ----------
    nombre : str
        Nombre del usuario.
    *args :
        Argumentos posicionales adicionales (teléfonos, códigos, etc.)
    rol : str, opcional
        Rol del usuario (default "usuario").
    **kwargs :
        Información adicional (ciudad, activo, email, etc.)

    Retorna:
    -------
    dict
        Diccionario con toda la información del usuario.

    Ejemplo:
    -------
    >>> crear_usuario("Ana", 123, rol="admin", activo=True)
    {'nombre': 'Ana', 'args': (123,), 'rol': 'admin', 'activo': True}
    """
    usuario = {"nombre": nombre, "args": args, "rol": rol}
    usuario.update(kwargs)
    return usuario

# =========================================================
# 3. Docstrings en clases
# =========================================================

class Usuario:
    """
    Representa un usuario en el sistema.

    Atributos:
    ----------
    nombre : str
        Nombre del usuario.
    rol : str
        Rol del usuario en el sistema.
    activo : bool
        Estado del usuario (activo/inactivo).

    Métodos:
    -------
    activar()
        Activa el usuario.
    desactivar()
        Desactiva el usuario.
    """

    def __init__(self, nombre: str, rol: str = "usuario", activo: bool = True):
        """Inicializa un usuario con nombre, rol y estado activo."""
        self.nombre = nombre
        self.rol = rol
        self.activo = activo

    def activar(self):
        """Marca el usuario como activo."""
        self.activo = True

    def desactivar(self):
        """Marca el usuario como inactivo."""
        self.activo = False

# =========================================================
# 4. Buenas prácticas para docstrings
# =========================================================

# - Usa el formato estándar de Python (PEP 257)
# - Documenta:
#   - Propósito de la función/clase/módulo
#   - Parámetros: tipo y descripción
#   - Retorno: tipo y descripción
#   - Excepciones que puede lanzar
#   - Ejemplos claros de uso
# - Para proyectos grandes, usar Sphinx o MkDocs para documentación automática
# - Mantener docstrings actualizados junto con el código
# - En APIs y pipelines, documentar todos los parámetros configurables y defaults
