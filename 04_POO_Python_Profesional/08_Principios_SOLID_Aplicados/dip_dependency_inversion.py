# dip_dependency_inversion.py

"""
DIP — Dependency Inversion Principle
-----------------------------------
“Los módulos de alto nivel NO deben depender
 de módulos de bajo nivel.
 Ambos deben depender de abstracciones.”

Y más importante todavía:
👉 Las abstracciones NO deben depender de los detalles.
👉 Los detalles deben depender de las abstracciones.

Este principio es EL NÚCLEO del diseño backend profesional.
Si no entiendes DIP, todo lo demás (SOLID, arquitectura, tests)
se cae como un castillo de naipes.
"""

# ============================================================
# ❌ MAL EJEMPLO: dependencia directa (violación de DIP)
# ============================================================

class MySQLDatabase:
    def save_user(self, user: dict) -> None:
        print("Usuario guardado en MySQL")


class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # ❌ dependencia directa

    def create_user(self, user: dict) -> None:
        self.db.save_user(user)


"""
PROBLEMAS GRAVES:
- UserService depende de una implementación concreta (MySQL)
- Si mañana usas PostgreSQL → rompes el servicio
- Imposible testear sin tocar base de datos real
- Alto acoplamiento
- CERO flexibilidad

Este es el típico código de estudiante que NO escala.
"""


# ============================================================
# 💥 CONSECUENCIAS REALES EN BACKEND
# ============================================================

"""
En proyectos reales esto provoca:
- Cambios caros
- Tests lentos o inexistentes
- Servicios imposibles de reutilizar
- Código rígido

En backend serio:
❌ No se crea la dependencia dentro del servicio
❌ No se depende de clases concretas
"""


# ============================================================
# ✅ APLICANDO DIP: dependemos de una ABSTRACCIÓN
# ============================================================

from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: dict) -> None:
        pass


"""
Esta abstracción:
- Define QUÉ se necesita
- NO define CÓMO se hace
- Es estable
- Es el contrato
"""


# ============================================================
# ✔️ IMPLEMENTACIONES (detalles)
# ============================================================

class MySQLUserRepository(UserRepository):
    def save(self, user: dict) -> None:
        print("Usuario guardado en MySQL")


class PostgresUserRepository(UserRepository):
    def save(self, user: dict) -> None:
        print("Usuario guardado en PostgreSQL")


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.data = []

    def save(self, user: dict) -> None:
        self.data.append(user)
        print("Usuario guardado en memoria (test)")


"""
Observa algo CLAVE:
- Las implementaciones dependen de la abstracción
- NO al revés
"""


# ============================================================
# 🔥 SERVICIO DE ALTO NIVEL (core del negocio)
# ============================================================

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository  # ✅ inyección de dependencia

    def create_user(self, user: dict) -> None:
        # lógica de negocio aquí
        self.repository.save(user)


"""
Ahora:
- UserService NO sabe si hay MySQL, Postgres o memoria
- Solo conoce el CONTRATO
- Esto es diseño limpio
"""


# ============================================================
# ✔️ USO REAL (producción vs tests)
# ============================================================

# Producción
repo_mysql = MySQLUserRepository()
service_prod = UserService(repo_mysql)
service_prod.create_user({"name": "Juan"})

# Cambio de base de datos SIN tocar el servicio
repo_pg = PostgresUserRepository()
service_prod_pg = UserService(repo_pg)
service_prod_pg.create_user({"name": "Ana"})

# Tests
repo_test = InMemoryUserRepository()
service_test = UserService(repo_test)
service_test.create_user({"name": "TestUser"})


"""
Cero cambios en UserService.
Esto es PODER ARQUITECTÓNICO.
"""


# ============================================================
# 🧪 TESTABILIDAD (por qué DIP es oro puro)
# ============================================================

def test_create_user():
    fake_repo = InMemoryUserRepository()
    service = UserService(fake_repo)

    service.create_user({"name": "Pepe"})

    assert fake_repo.data[0]["name"] == "Pepe"


"""
Gracias a DIP:
- Tests rápidos
- Sin mocks complejos
- Sin frameworks mágicos
- Código predecible
"""


# ============================================================
# 🧠 DIP EN BACKEND REAL (arquitectura por capas)
# ============================================================

"""
Arquitectura típica limpia:

[ API / Controllers ]
          ↓
[ Services / Use Cases ]  ← depende de interfaces
          ↓
[ Repositories (interfaces) ]
          ↓
[ Infraestructura (SQL, APIs, Redis, etc.) ]

La dirección de dependencia SIEMPRE apunta hacia el núcleo.
"""


# ============================================================
# 🚫 ERRORES COMUNES (muy típicos)
# ============================================================

"""
❌ new MySQLRepository() dentro del servicio
❌ importar frameworks en el dominio
❌ lógica de negocio dependiendo de ORM
❌ acoplar código a librerías externas

Si ves eso:
→ DIP roto
"""


# ============================================================
# 🎯 CONEXIÓN DIRECTA CON TU OBJETIVO (backend + IA)
# ============================================================

"""
DIP es CLAVE para:
- Microservicios
- Pipelines de datos
- Sistemas ML (cambiar modelo sin romper lógica)
- Arquitecturas escalables
- Código profesional de verdad

Ejemplo en ML:
- Servicio depende de ModelPredictor (interfaz)
- Implementación puede ser sklearn, pytorch, mock, etc.

Si dominas DIP:
➡️ Diseñas sistemas intercambiables
➡️ Tu código envejece bien
➡️ Piensas como ingeniero senior

Esto NO es teoría.
Esto es supervivencia en proyectos reales.
"""
