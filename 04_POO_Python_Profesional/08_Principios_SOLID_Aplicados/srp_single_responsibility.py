# srp_single_responsibility.py

"""
Single Responsibility Principle (SRP)
--------------------------------------
Cada clase debe tener una única responsabilidad, una sola razón para cambiar.
Esto reduce acoplamientos, facilita testing y hace el código más mantenible.
En proyectos de backend y data, SRP es clave para separar lógica de negocio,
persistencia y notificaciones, evitando clases “multipropósito” difíciles de mantener.
"""

# ❌ Ejemplo de mala práctica: clase con múltiples responsabilidades
class UsuarioManager:
    def __init__(self, usuario):
        self.usuario = usuario

    def validar_usuario(self):
        # Validaciones complejas
        pass

    def guardar_en_db(self):
        # Lógica de persistencia
        pass

    def enviar_email_bienvenida(self):
        # Lógica de notificación
        pass


# ✅ Ejemplo aplicando SRP: separar responsabilidades

class UsuarioValidator:
    """Responsable únicamente de validar usuarios"""
    @staticmethod
    def validar(usuario):
        # Implementar reglas de validación
        print(f"Validando usuario {usuario}")


class UsuarioRepository:
    """Responsable únicamente de guardar usuarios en la base de datos"""
    def guardar(self, usuario):
        # Código de persistencia
        print(f"Guardando usuario {usuario} en la base de datos")


class EmailService:
    """Responsable únicamente de enviar emails"""
    @staticmethod
    def enviar_bienvenida(usuario):
        # Código de envío de correo
        print(f"Enviando email de bienvenida a {usuario}")


# Uso práctico en backend
if __name__ == "__main__":
    usuario = "Juan Perez"

    # Cada clase hace solo lo que le corresponde
    UsuarioValidator.validar(usuario)
    repo = UsuarioRepository()
    repo.guardar(usuario)
    EmailService.enviar_bienvenida(usuario)
