# repository_pattern.py

"""
REPOSITORY PATTERN — Acceso a datos limpio
=========================================

Este patrón es FUNDAMENTAL.
Si Strategy te hace pensar como arquitecto,
Repository te hace pensar como BACKEND PROFESIONAL REAL.

Repository sirve para:
✅ Separar lógica de negocio de la persistencia
✅ Poder cambiar BD sin tocar el dominio
✅ Facilitar tests (mockear datos)
✅ Aplicar SOLID (SRP + DIP)
✅ Diseñar sistemas escalables y mantenibles

Esto es CORE en:
- Backends profesionales
- Arquitecturas limpias
- Microservicios
- Sistemas de datos
- Proyectos serios (no scripts)
"""

# ============================================================
# ❌ PROBLEMA REAL SIN REPOSITORY
# ============================================================

class UsuarioService_MAL:
    def crear_usuario(self, nombre: str):
        # lógica de negocio mezclada con SQL
        print("INSERT INTO usuarios (nombre) VALUES (...)")
        # ¿y si cambiamos SQL por Mongo? ¿o API externa?
        # código acoplado = infierno


"""
Problemas GRAVES:
- SQL mezclado con negocio
- Imposible testear sin BD
- Cambiar BD rompe todo
- Violación SRP y DIP
"""

# ============================================================
# 🧠 IDEA CLAVE DEL REPOSITORY PATTERN
# ============================================================

"""
Separar:
- EL DOMINIO (qué es un Usuario)
- DE CÓMO se guarda / obtiene

El dominio NO sabe:
- si hay SQL
- si hay Mongo
- si hay API
- si hay memoria

Solo sabe que hay un repositorio.
"""

# ============================================================
# 🧱 ENTIDAD DE DOMINIO (PURO)
# ============================================================

class Usuario:
    def __init__(self, id_: int, nombre: str):
        self.id = id_
        self.nombre = nombre

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}')"


"""
Regla CLAVE:
- El dominio NO conoce SQL, JSON, requests, etc.
"""

# ============================================================
# 📜 CONTRATO DEL REPOSITORIO (INTERFAZ)
# ============================================================

from abc import ABC, abstractmethod


class UsuarioRepository(ABC):

    @abstractmethod
    def guardar(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id_: int) -> Usuario | None:
        pass

    @abstractmethod
    def listar(self) -> list[Usuario]:
        pass


"""
Esto es CRÍTICO:
- El dominio depende de la ABSTRACCIÓN
- No de la implementación concreta
(DIP real)
"""

# ============================================================
# 🧩 IMPLEMENTACIÓN 1: Repositorio en memoria (tests / dev)
# ============================================================

class UsuarioRepositoryInMemory(UsuarioRepository):
    def __init__(self):
        self._data: dict[int, Usuario] = {}

    def guardar(self, usuario: Usuario) -> None:
        self._data[usuario.id] = usuario

    def obtener_por_id(self, id_: int) -> Usuario | None:
        return self._data.get(id_)

    def listar(self) -> list[Usuario]:
        return list(self._data.values())


# ============================================================
# 🧩 IMPLEMENTACIÓN 2: Repositorio SQL (simulado)
# ============================================================

class UsuarioRepositorySQL(UsuarioRepository):
    def guardar(self, usuario: Usuario) -> None:
        print(f"[SQL] INSERT usuario {usuario}")

    def obtener_por_id(self, id_: int) -> Usuario | None:
        print(f"[SQL] SELECT usuario WHERE id={id_}")
        return Usuario(id_, "MockSQL")

    def listar(self) -> list[Usuario]:
        print("[SQL] SELECT * FROM usuarios")
        return [Usuario(1, "SQL_User")]


"""
Fíjate:
- La interfaz es la misma
- El dominio NO cambia
"""

# ============================================================
# 🚀 SERVICIO DE NEGOCIO (USA EL REPOSITORY)
# ============================================================

class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def registrar_usuario(self, id_: int, nombre: str):
        usuario = Usuario(id_, nombre)
        self.repo.guardar(usuario)

    def obtener_usuario(self, id_: int) -> Usuario | None:
        return self.repo.obtener_por_id(id_)

    def listar_usuarios(self) -> list[Usuario]:
        return self.repo.listar()


"""
Este servicio:
- NO sabe si hay SQL
- NO sabe si hay Mongo
- NO sabe si hay API
"""

# ============================================================
# ✅ USO REAL
# ============================================================

repo_memoria = UsuarioRepositoryInMemory()
service = UsuarioService(repo_memoria)

service.registrar_usuario(1, "Alex")
service.registrar_usuario(2, "Lucía")

print(service.obtener_usuario(1))
print(service.listar_usuarios())


repo_sql = UsuarioRepositorySQL()
service_sql = UsuarioService(repo_sql)

service_sql.registrar_usuario(10, "Empresa")
print(service_sql.obtener_usuario(10))


# ============================================================
# 🧠 REPOSITORY EN BACKEND REAL
# ============================================================

"""
En backend serio:
- 1 repositorio por agregado (Usuario, Pedido, Producto)
- El repositorio SOLO accede a datos
- NO hay lógica de negocio dentro

Ejemplos:
- UsuarioRepository
- PedidoRepository
- PagoRepository
"""

# ============================================================
# 🧠 REPOSITORY EN DATA / IA (MUY IMPORTANTE)
# ============================================================

"""
En data / ML:
- Acceso a datasets
- Features
- Modelos entrenados
"""

class DatasetRepository(ABC):
    @abstractmethod
    def cargar(self):
        pass


class CSVDatasetRepository(DatasetRepository):
    def cargar(self):
        print("Cargando datos desde CSV")
        return [1, 2, 3]


class APIDatasetRepository(DatasetRepository):
    def cargar(self):
        print("Cargando datos desde API")
        return [4, 5, 6]


class DataService:
    def __init__(self, repo: DatasetRepository):
        self.repo = repo

    def obtener_datos(self):
        return self.repo.cargar()


"""
Esto te permite:
- cambiar fuente de datos
- testear sin APIs reales
- escalar pipelines
"""

# ============================================================
# ⚠️ ERRORES COMUNES
# ============================================================

"""
❌ Meter lógica de negocio en el repositorio
❌ Devolver dicts en vez de entidades
❌ Hacer repositorios gigantes
❌ Saltarse la interfaz "porque es más rápido"
"""

# ============================================================
# 🎯 CONCLUSIÓN CLARA (sin humo)
# ============================================================

"""
Repository NO es opcional en backend serio.

Si NO lo usas:
- código acoplado
- tests imposibles
- refactors dolorosos

Si lo usas bien:
- dominio limpio
- código mantenible
- arquitectura profesional
- preparado para crecer

Este patrón es OBLIGATORIO para tu futuro.
"""

