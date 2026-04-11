# solid_introduccion.md

## Qué es SOLID y por qué importa

SOLID es un acrónimo que engloba cinco principios de diseño orientado a objetos pensados para mejorar la calidad, mantenibilidad y escalabilidad del software. Estos principios son especialmente importantes en proyectos de backend y data, donde los sistemas tienden a crecer y complejizarse rápidamente.

---

### S → Single Responsibility Principle (SRP)
**Principio de Responsabilidad Única:**  
Cada clase o módulo debe tener una única razón para cambiar.  
**Por qué importa:** Facilita testing, mantenimiento y reduce acoplamientos innecesarios.  
**Ejemplo real (backend):**

```python
# ❌ Mala práctica: la clase hace demasiado
class UsuarioManager:
    def validar_usuario(self, usuario): ...
    def enviar_email_bienvenida(self, usuario): ...
    def guardar_usuario_db(self, usuario): ...

# ✅ Buena práctica: SRP, responsabilidades separadas
class UsuarioValidator:
    def validar(self, usuario): ...

class EmailService:
    def enviar_bienvenida(self, usuario): ...

class UsuarioRepository:
    def guardar(self, usuario): ...
```
---
### O → Open/Closed Principle (OCP)
Principio de Abierto/Cerrado:
Las clases deben estar abiertas para extensión pero cerradas para modificación.
Por qué importa: Permite añadir funcionalidades sin tocar código existente, evitando bugs.
Ejemplo:

```python
# Base cerrada a cambios, abierta a extensiones
class Descuento:
    def calcular(self, total: float) -> float:
        return total

class DescuentoVIP(Descuento):
    def calcular(self, total: float) -> float:
        return total * 0.8
```
---
### L → Liskov Substitution Principle (LSP)
Principio de Sustitución de Liskov:
Los objetos de una subclase deben poder reemplazar a los de la superclase sin romper la lógica del programa.
Por qué importa: Garantiza coherencia y seguridad al usar herencia.
Ejemplo:

```python
class Forma:
    def area(self) -> float:
        pass

class Rectangulo(Forma):
    def area(self) -> float:
        return self.ancho * self.alto

class Cuadrado(Rectangulo):
    def area(self) -> float:
        # ⚠️ Evitar romper comportamiento esperado de Rectangulo
        return self.lado * self.lado
```
---
### I → Interface Segregation Principle (ISP)
Principio de Segregación de Interfaces:
Es mejor tener varias interfaces pequeñas y específicas que una grande y genérica.
Por qué importa: Las clases implementan solo lo que necesitan, evitando métodos vacíos o irrelevantes.
Ejemplo:

```python
class IEmailSender(ABC):
    @abstractmethod
    def enviar_email(self, mensaje): ...

class ISMSender(ABC):
    @abstractmethod
    def enviar_sms(self, mensaje): ...
```
---
### D → Dependency Inversion Principle (DIP)
Principio de Inversión de Dependencias:
Las dependencias deben apuntar a abstracciones, no a implementaciones concretas.
Por qué importa: Facilita testing, mantenimiento y desacoplamiento.
Ejemplo (backend):

```python
class RepositorioUsuarios(ABC):
    @abstractmethod
    def guardar(self, usuario): ...

class UsuarioService:
    def __init__(self, repo: RepositorioUsuarios):
        self.repo = repo

    def crear_usuario(self, usuario):
        self.repo.guardar(usuario)
```
---
### Conclusión
Aplicar SOLID te ayuda a crear código:

Más legible y mantenible.

Fácil de probar y extender.

Robusto frente a cambios futuros.

>En tu camino hacia backend profesional y data, dominar estos principios desde ya te evitará que tus proyectos se conviertan en un "código spaghetti" inmantenible.