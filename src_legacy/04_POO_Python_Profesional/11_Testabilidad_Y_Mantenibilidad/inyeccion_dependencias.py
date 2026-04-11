# inyeccion_dependencias.py

"""
INYECCIÓN DE DEPENDENCIAS EN PYTHON
===================================

Objetivo:
---------
Demostrar cómo desacoplar componentes en Python sin usar frameworks,
permitiendo reemplazar implementaciones concretas con mocks o stubs
en tests y facilitando la mantenibilidad.

Conceptos clave:
----------------
1. Inversión de control: las dependencias se pasan desde fuera, no se crean dentro.
2. Interfaces abstractas o protocolos: definir contratos claros para los componentes.
3. Flexibilidad y testabilidad: podemos cambiar implementaciones sin tocar la clase.
"""

# ============================================================
# Ejemplo: servicio que depende de un repositorio
# ============================================================

from typing import Protocol, List
from dataclasses import dataclass

# Definimos un protocolo que actúa como "interfaz"
class RepositorioUsuarios(Protocol):
    def listar_todos(self) -> List[str]:
        ...

# Implementación concreta
class RepositorioUsuariosSQL:
    def listar_todos(self) -> List[str]:
        # Imaginemos que consulta una base de datos
        return ["Alice", "Bob", "Charlie"]

# Servicio que recibe la dependencia
class ServicioUsuarios:
    def __init__(self, repo: RepositorioUsuarios):
        self.repo = repo

    def obtener_nombres(self) -> List[str]:
        return self.repo.listar_todos()


# ============================================================
# Ejemplo de inyección de dependencias para test
# ============================================================

class RepositorioUsuariosMock:
    """Mock para pruebas sin base de datos real"""
    def listar_todos(self) -> List[str]:
        return ["TestUser1", "TestUser2"]

# ============================================================
# Uso práctico
# ============================================================

if __name__ == "__main__":
    # Inyección de implementación real
    servicio_real = ServicioUsuarios(RepositorioUsuariosSQL())
    print("Nombres reales:", servicio_real.obtener_nombres())

    # Inyección de mock para tests
    servicio_test = ServicioUsuarios(RepositorioUsuariosMock())
    print("Nombres de test:", servicio_test.obtener_nombres())

"""
Explicación orientada a tu caso:
--------------------------------
En proyectos de backend o pipelines de datos, muchas clases dependen
de repositorios, APIs o servicios externos. Aplicando inyección de dependencias:

- Nunca acoplas la clase a una base de datos específica.
- Puedes probar la lógica de negocio sin necesidad de una DB real.
- Facilita el mantenimiento y escalabilidad del sistema.

Esto es crucial si quieres escribir código profesional y testable,
como mencionaste que deseas para tus proyectos y aprendizaje de POO.
"""
