# refactor_herencia_a_composicion.py
# Ejemplo de cómo refactorizar un diseño basado en herencia hacia composición en un caso real

"""
Supongamos que tenemos una aplicación de notificaciones que originalmente usaba herencia:

class Notificador:
    def enviar(self, mensaje):
        pass

class EmailNotificador(Notificador):
    def enviar(self, mensaje):
        print(f"Enviando Email: {mensaje}")

class SMSNotificador(Notificador):
    def enviar(self, mensaje):
        print(f"Enviando SMS: {mensaje}")

Problema:
- Cada vez que añadimos un canal de notificación, necesitamos crear una subclase.
- Si queremos combinar comportamientos (por ejemplo, enviar Email + SMS), la herencia se complica.
- Rompe el principio de abierto/cerrado y genera jerarquías rígidas.
"""

# -------------------------------------------------
# REFACTOR: Composición
# -------------------------------------------------
class NotificadorEmail:
    def enviar(self, mensaje):
        print(f"Enviando Email: {mensaje}")

class NotificadorSMS:
    def enviar(self, mensaje):
        print(f"Enviando SMS: {mensaje}")

class GestorNotificaciones:
    """
    Gestor de notificaciones que "tiene" múltiples notificadores.
    La composición permite combinar comportamientos fácilmente.
    """
    def __init__(self, notificadores):
        self.notificadores = notificadores  # Lista de objetos notificador

    def enviar_todas(self, mensaje):
        for notificador in self.notificadores:
            notificador.enviar(mensaje)

# -------------------------------------------------
# USO REAL
# -------------------------------------------------
email = NotificadorEmail()
sms = NotificadorSMS()

gestor = GestorNotificaciones([email, sms])
gestor.enviar_todas("Hola, este es un mensaje importante")

# Salida esperada:
# Enviando Email: Hola, este es un mensaje importante
# Enviando SMS: Hola, este es un mensaje importante

# -------------------------------------------------
# LECCIONES
# -------------------------------------------------
"""
- Evitamos herencia innecesaria y rígida.
- Podemos agregar nuevos canales de notificación sin modificar GestorNotificaciones.
- Facilita testing: se pueden inyectar mocks de notificador.
- Cumple el principio de abierto/cerrado (OCP) y Single Responsibility (SRP).
"""
