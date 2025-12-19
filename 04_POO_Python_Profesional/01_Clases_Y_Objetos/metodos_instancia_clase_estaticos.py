# metodos_instancia_clase_estaticos.py
# @classmethod y @staticmethod en Python
# Orientado a backend y proyectos de datos

"""
En Python existen tres tipos de métodos en una clase:

1. Métodos de instancia: reciben `self`, acceden a atributos de esa instancia.
2. Métodos de clase: reciben `cls`, acceden a atributos de clase.
3. Métodos estáticos: no reciben ni `self` ni `cls`, funcionan como funciones independientes, pero organizadas dentro de la clase.
Esto es útil para estructurar lógica de manera profesional y clara.
"""

# -------------------------------------------------
# 1. Método de instancia
# -------------------------------------------------
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

    def saludo(self):
        """Accede a datos de la instancia"""
        return f"Hola, soy {self.nombre}"

usuario = Usuario("Ana", "ana@email.com")
print(usuario.saludo())  # Hola, soy Ana

# -------------------------------------------------
# 2. Método de clase
# -------------------------------------------------
class Configuracion:
    version = "1.0"

    @classmethod
    def actualizar_version(cls, nueva_version: str):
        """Accede/modifica atributos de clase"""
        cls.version = nueva_version

config1 = Configuracion()
config2 = Configuracion()

Configuracion.actualizar_version("2.0")
print(config1.version)  # 2.0
print(config2.version)  # 2.0

# Ejemplo práctico: crear instancias desde datos alternativos
class UsuarioFactory:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    @classmethod
    def desde_dict(cls, data: dict):
        """Crear usuario a partir de diccionario"""
        return cls(data["nombre"], data["email"])

data_usuario = {"nombre": "Luis", "email": "luis@email.com"}
usuario2 = UsuarioFactory.desde_dict(data_usuario)
print(usuario2.nombre)  # Luis

# -------------------------------------------------
# 3. Método estático
# -------------------------------------------------
class Utilidades:
    @staticmethod
    def es_email_valido(email: str) -> bool:
        """Valida sin usar atributos de clase ni instancia"""
        return "@" in email and "." in email

print(Utilidades.es_email_valido("ana@email.com"))  # True
print(Utilidades.es_email_valido("invalido-email"))  # False

# Ejemplo en backend:
# Comprobaciones, utilidades de formato o validaciones que no necesitan datos de la clase se colocan como staticmethod.
# Esto mantiene la lógica organizada y evita funciones sueltas fuera de contexto.

# -------------------------------------------------
# 4. Resumen de uso
# -------------------------------------------------
"""
- Método de instancia: accede a datos de un objeto concreto (`self`).
- Método de clase: accede a datos compartidos entre todos los objetos (`cls`), útil para fábrica de objetos o configuración global.
- Método estático: lógica que no depende ni del objeto ni de la clase, pero conceptualmente pertenece a la clase.
- Buen patrón: mantener la responsabilidad y la claridad de cada método según su tipo.
"""
