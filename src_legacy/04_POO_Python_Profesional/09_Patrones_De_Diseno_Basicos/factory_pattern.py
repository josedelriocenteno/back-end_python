# factory_pattern.py

"""
FACTORY PATTERN — Creación controlada de objetos
================================================

Este patrón SOLUCIONA uno de los mayores errores de principiantes:
👉 crear objetos directamente con lógica repartida por todo el sistema.

Si no usas factories:
- if/else por todos lados
- código acoplado
- clases que saben demasiado
- cambios dolorosos

La Factory NO es un patrón “bonito”.
Es un patrón de SUPERVIVENCIA en backend real.
"""

# ============================================================
# ❌ MAL DISEÑO: creación directa y acoplada
# ============================================================

class EmailNotification:
    def send(self, message: str) -> None:
        print(f"Enviando EMAIL: {message}")


class SMSNotification:
    def send(self, message: str) -> None:
        print(f"Enviando SMS: {message}")


class PushNotification:
    def send(self, message: str) -> None:
        print(f"Enviando PUSH: {message}")


def notify_user(channel: str, message: str) -> None:
    if channel == "email":
        notifier = EmailNotification()
    elif channel == "sms":
        notifier = SMSNotification()
    elif channel == "push":
        notifier = PushNotification()
    else:
        raise ValueError("Canal no soportado")

    notifier.send(message)


"""
PROBLEMAS REALES:
- Cada nuevo canal ⇒ modificar esta función
- Violación directa de OCP
- La lógica de creación está mezclada con lógica de negocio
- Código frágil y poco escalable
"""


# ============================================================
# 🧠 IDEA CLAVE DEL FACTORY PATTERN
# ============================================================

"""
Separar:
- QUÉ se crea (decisión)
- CÓMO se usa (lógica de negocio)

El código que usa el objeto NO debería decidir
qué clase concreta instanciar.
"""


# ============================================================
# ✅ PASO 1: Definir una abstracción común
# ============================================================

from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


# ============================================================
# ✅ PASO 2: Implementaciones concretas
# ============================================================

class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Enviando EMAIL: {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Enviando SMS: {message}")


class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Enviando PUSH: {message}")


"""
Nada especial aquí.
Lo importante viene ahora.
"""


# ============================================================
# 🔥 FACTORY SIMPLE (centraliza la creación)
# ============================================================

class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        if channel == "email":
            return EmailNotification()
        elif channel == "sms":
            return SMSNotification()
        elif channel == "push":
            return PushNotification()
        else:
            raise ValueError("Canal no soportado")


"""
AHORA:
- Un solo punto de creación
- El resto del sistema NO conoce las clases concretas
- El if/else vive en un único sitio (controlado)
"""


# ============================================================
# ✅ USO CORRECTO EN LÓGICA DE NEGOCIO
# ============================================================

def notify_user(channel: str, message: str) -> None:
    notifier = NotificationFactory.create(channel)
    notifier.send(message)


notify_user("email", "Hola")
notify_user("sms", "Código 1234")


"""
La función:
- NO sabe qué clase se usa
- Solo usa la interfaz
- Mucho más limpia
"""


# ============================================================
# 🚀 FACTORY + DIP (nivel profesional)
# ============================================================

"""
En backend serio:
- El servicio NO debería depender ni siquiera de la factory concreta
- La factory también se inyecta
"""

class NotificationService:
    def __init__(self, factory):
        self.factory = factory

    def notify(self, channel: str, message: str) -> None:
        notifier = self.factory.create(channel)
        notifier.send(message)


service = NotificationService(NotificationFactory)
service.notify("push", "Nueva alerta")


# ============================================================
# 🧪 TESTABILIDAD (por qué las factories importan)
# ============================================================

class FakeNotification(Notification):
    def __init__(self):
        self.sent_messages = []

    def send(self, message: str) -> None:
        self.sent_messages.append(message)


class FakeNotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        return FakeNotification()


def test_notification_service():
    service = NotificationService(FakeNotificationFactory)
    service.notify("email", "Test")

    notifier = service.factory.create("email")
    assert "Test" in notifier.sent_messages


"""
Gracias a la factory:
- Tests sin dependencias externas
- Sin if/else hackeados
- Código limpio
"""


# ============================================================
# ⚠️ ERROR COMÚN: Factory mal entendida
# ============================================================

"""
❌ Factory que hace lógica de negocio
❌ Factory gigante con 200 if/else sin sentido
❌ Usar factory para TODO (overengineering)

La factory SOLO debe:
➡️ decidir QUÉ objeto crear
"""


# ============================================================
# 🧠 CUÁNDO USAR FACTORY (regla práctica)
# ============================================================

"""
Usa Factory cuando:
✔️ Hay múltiples implementaciones posibles
✔️ La creación NO es trivial
✔️ El tipo depende de configuración, input o contexto
✔️ Quieres desacoplar lógica de negocio

NO la uses cuando:
❌ Solo hay una clase
❌ new Clase() es trivial y estable
"""


# ============================================================
# 🎯 CONEXIÓN DIRECTA CON TU PERFIL (backend + IA)
# ============================================================

"""
En IA / Data / Backend usarás factories para:
- Crear modelos (RandomForest, XGBoost, NN…)
- Crear pipelines
- Crear clientes de APIs
- Crear repositorios
- Crear estrategias de inferencia

Ejemplo real:
ModelFactory.create("sklearn")
ModelFactory.create("pytorch")

SIN tocar el resto del sistema.

Si dominas Factory:
➡️ Tu código escala
➡️ Cambias tecnología sin dolor
➡️ Piensas como ingeniero profesional

Este patrón NO es opcional.
Es básico en sistemas reales.
"""
