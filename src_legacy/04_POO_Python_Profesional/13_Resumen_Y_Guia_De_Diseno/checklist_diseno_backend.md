# Checklist de Diseño Backend Profesional con POO

Este checklist está orientado a asegurar que el diseño de tus sistemas backend cumpla buenas prácticas de POO profesional, escalabilidad y mantenibilidad.

---

## 1️⃣ Clases y Objetos
- [ ] Cada clase tiene una única responsabilidad (SRP).
- [ ] Los nombres de clases y atributos son descriptivos.
- [ ] Atributos de instancia vs clase correctamente diferenciados.
- [ ] Uso adecuado de métodos de instancia, clase y estáticos (`@classmethod`, `@staticmethod`).

---

## 2️⃣ Encapsulación y Abstracción
- [ ] Los atributos sensibles están protegidos (`_protected`, `__private`).
- [ ] Se utilizan `@property` y setters para validación de datos.
- [ ] Interfaces abstractas o clases base definidas cuando conviene.
- [ ] No existen clases “anémicas” o getters/setters innecesarios.

---

## 3️⃣ Herencia y Composición
- [ ] Herencia usada solo cuando hay una relación clara "Es un".
- [ ] Composición preferida cuando la relación es "Tiene un".
- [ ] Evitar herencia múltiple a menos que sea segura y necesaria.
- [ ] Revisar MRO para asegurar comportamiento correcto en herencia compleja.

---

## 4️⃣ Clases Inmutables y Value Objects
- [ ] Value Objects inmutables donde se requiera seguridad y predictibilidad.
- [ ] Uso de `@dataclass(frozen=True)` para objetos que no deben cambiar.
- [ ] Los objetos son hashables si se usan en sets o como claves de diccionario.

---

## 5️⃣ Métodos Especiales (Dunder)
- [ ] Implementados `__str__` y `__repr__` para debugging.
- [ ] Implementados `__eq__` y `__hash__` si la clase será comparable o hashable.
- [ ] Comparadores (`__lt__`, `__gt__`) solo si la ordenación es relevante.
- [ ] Otros métodos como `__call__`, `__len__`, `__iter__` usados para mejorar la interfaz del objeto.

---

## 6️⃣ Principios SOLID
- [ ] SRP: Cada clase tiene solo una responsabilidad.
- [ ] OCP: Las extensiones se realizan sin modificar clases existentes.
- [ ] LSP: Los subtipo reemplazan correctamente al tipo base.
- [ ] ISP: Interfaces pequeñas, enfocadas y específicas.
- [ ] DIP: Las clases de alto nivel dependen de abstracciones, no de implementaciones concretas.

---

## 7️⃣ Patrones de Diseño
- [ ] Factory Pattern para creación controlada de objetos.
- [ ] Singleton solo si es estrictamente necesario.
- [ ] Strategy Pattern para algoritmos intercambiables.
- [ ] Repository Pattern para acceso a datos desacoplado.
- [ ] Service Layer para encapsular lógica de negocio y mantener control de flujo.

---

## 8️⃣ Backend y Arquitectura de Capas
- [ ] Separación clara de capas: Domain, Application, Infrastructure.
- [ ] Modelos del dominio claros y concisos.
- [ ] Servicios y repositorios desacoplados para facilitar testabilidad.
- [ ] Aplicación de Value Objects, composición y principios SOLID en toda la arquitectura.

---

## 9️⃣ Testabilidad y Mantenibilidad
- [ ] Clases fáciles de testear y desacopladas.
- [ ] Inyección de dependencias aplicada correctamente.
- [ ] Uso de mocks y stubs para aislar dependencias externas en tests.
- [ ] Código modular y con responsabilidades bien delimitadas.

---

## 10️⃣ Buenas Prácticas Generales
- [ ] Código limpio, legible y consistente.
- [ ] Evitar duplicación y código espagueti.
- [ ] Documentación con docstrings claros y útiles.
- [ ] Revisar complejidad y mantener la simplicidad del diseño.

---

Este checklist se puede usar como referencia antes de finalizar un módulo o proyecto, asegurando que se han aplicado los principios de POO profesional y las buenas prácticas de backend.
