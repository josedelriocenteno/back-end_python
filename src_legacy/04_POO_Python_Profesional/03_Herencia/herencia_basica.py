# herencia_basica.py
# Ejemplo de herencia básica en Python orientada a backend y modelos de datos

"""
La herencia permite crear nuevas clases a partir de clases existentes.
Beneficios:
- Reutilización de código
- Extensión de funcionalidades
- Modelado más natural de entidades relacionadas

Cuidado: no abusar de la herencia, puede generar jerarquías rígidas.
"""

# -------------------------------------------------
# CLASE BASE
# -------------------------------------------------
class Usuario:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def enviar_email(self, mensaje):
        print(f"Enviando email a {self.email}: {mensaje}")

# -------------------------------------------------
# CLASE DERIVADA (HERENCIA)
# -------------------------------------------------
class Administrador(Usuario):
    def __init__(self, nombre, email, permisos):
        # Reutilizamos inicialización de la clase base
        super().__init__(nombre, email)
        self.permisos = permisos

    def agregar_permiso(self, permiso):
        self.permisos.append(permiso)
        print(f"Permiso '{permiso}' agregado a {self.nombre}")

# -------------------------------------------------
# USO
# -------------------------------------------------
admin = Administrador("Carlos", "carlos@empresa.com", ["leer", "escribir"])
admin.enviar_email("Bienvenido al sistema")  # Método heredado
admin.agregar_permiso("borrar")             # Método propio

# -------------------------------------------------
# Buenas prácticas
# -------------------------------------------------
"""
1. Usa herencia solo si existe una relación "es un" clara:
   Administrador ES un Usuario.
2. Evita herencias profundas (>3 niveles) para mantener mantenibilidad.
3. Usa super() para inicializar correctamente la clase base.
4. Sobrescribe métodos solo cuando sea necesario extender o modificar comportamiento.
"""
