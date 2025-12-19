# Reglas de decisión: Composición vs Herencia

Cuando diseñamos sistemas orientados a objetos en Python (y en general), elegir entre **herencia** y **composición** es crítico para mantener código flexible, mantenible y profesional. Aquí tienes reglas claras basadas en buenas prácticas de backend y data:

---

## 1. Usa **Herencia** cuando:

- Existe una relación clara de "**es un**" entre clases.
  - Ejemplo: `class Perro(Mamifero)`. Un perro **es un** mamífero.
- Quieres reutilizar implementación base.
- La jerarquía es estable y no cambiará con frecuencia.
- Todas las subclases comparten la mayoría del comportamiento de la clase base.

**Advertencias:**
- Evita herencia múltiple a menos que sepas exactamente cómo Python resuelve MRO.
- No abuses de herencia solo para compartir métodos: puede romper SRP y OCP.

---

## 2. Usa **Composición** cuando:

- La relación es "**tiene un**" o "**usa un**".
  - Ejemplo: `class Coche` que **tiene un** `Motor`.
- Necesitas flexibilidad para combinar comportamientos.
  - Ejemplo: gestor de notificaciones que puede enviar Email + SMS.
- Quieres desacoplar componentes y facilitar testing.
- Quieres cumplir principios SOLID: OCP y SRP.

**Beneficios:**
- Agregar nuevas funcionalidades no rompe código existente.
- Facilita inyección de dependencias y mocks.
- Evita jerarquías rígidas y frágiles.

---

## 3. Reglas rápidas de decisión

| Situación                                      | Herencia | Composición |
|-----------------------------------------------|----------|-------------|
| Relación clara "es un"                        | ✅       | ❌          |
| Relación "tiene un" o "usa un"               | ❌       | ✅          |
| Reutilizar código base estable                 | ✅       | ✅ (delegando) |
| Necesidad de combinar múltiples comportamientos | ❌      | ✅          |
| Código que debe ser fácil de testear          | ❌       | ✅          |
| Jerarquías que cambiarán con frecuencia       | ❌       | ✅          |

---

## 4. Ejemplo práctico rápido

```python
# Herencia rígida (menos flexible)
class Notificador:
    def enviar(self, mensaje):
        pass

class EmailNotificador(Notificador):
    def enviar(self, mensaje):
        print(f"Email: {mensaje}")

class SMSNotificador(Notificador):
    def enviar(self, mensaje):
        print(f"SMS: {mensaje}")

# Composición flexible
class GestorNotificaciones:
    def __init__(self, notificadores):
        self.notificadores = notificadores

    def enviar_todas(self, mensaje):
        for n in self.notificadores:
            n.enviar(mensaje)

email = EmailNotificador()
sms = SMSNotificador()
gestor = GestorNotificaciones([email, sms])
gestor.enviar_todas("Mensaje importante")
