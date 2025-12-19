# isp_interface_segregation.py

"""
ISP — Interface Segregation Principle
------------------------------------
“Los clientes NO deben verse forzados a depender
de interfaces que no utilizan.”

Traducción clara y directa:
👉 Es mejor tener MUCHAS interfaces pequeñas y específicas
   que UNA interfaz gigante y genérica.

Este principio es CLAVE en backend profesional.
Romperlo genera código rígido, frágil y lleno de hacks.
"""

# ============================================================
# ❌ MAL EJEMPLO: interfaz gorda (violación de ISP)
# ============================================================

from abc import ABC, abstractmethod


class RepositorioUsuarios(ABC):
    @abstractmethod
    def crear(self, data: dict) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def eliminar(self, user_id: int) -> None:
        pass

    @abstractmethod
    def exportar_csv(self) -> str:
        pass


"""
PROBLEMA:
- Esta interfaz mezcla responsabilidades
- Obliga a TODAS las implementaciones a soportar TODO
- Aunque no tenga sentido
"""


class RepositorioUsuariosReadOnly(RepositorioUsuarios):
    def crear(self, data: dict) -> None:
        raise NotImplementedError()

    def obtener_por_id(self, user_id: int) -> dict:
        return {"id": user_id}

    def eliminar(self, user_id: int) -> None:
        raise NotImplementedError()

    def exportar_csv(self) -> str:
        raise NotImplementedError()


"""
💥 ESTO ES UNA VIOLACIÓN CLARA DE ISP

- La clase está FORZADA a implementar métodos inútiles
- Aparecen NotImplementedError (olor a diseño malo)
- Los clientes deben "adivinar" qué se puede usar

Si ves NotImplementedError en producción → algo está mal.
"""


# ============================================================
# 💣 POR QUÉ ESTO ES GRAVE EN BACKEND REAL
# ============================================================

"""
En sistemas reales esto provoca:
- Servicios que solo usan 1 método pero dependen de 5
- Cambios pequeños rompen muchas clases
- Tests innecesariamente complejos
- Interfaces imposibles de reutilizar

Resultado:
❌ Código frágil
❌ Acoplamiento innecesario
❌ Mala escalabilidad del diseño
"""


# ============================================================
# ✅ SOLUCIÓN CORRECTA: interfaces pequeñas y cohesionadas
# ============================================================

class UsuarioReader(ABC):
    @abstractmethod
    def obtener_por_id(self, user_id: int) -> dict:
        pass


class UsuarioWriter(ABC):
    @abstractmethod
    def crear(self, data: dict) -> None:
        pass


class UsuarioDeleter(ABC):
    @abstractmethod
    def eliminar(self, user_id: int) -> None:
        pass


class UsuarioExporter(ABC):
    @abstractmethod
    def exportar_csv(self) -> str:
        pass


"""
Ahora:
- Cada interfaz tiene UNA responsabilidad clara
- Nadie depende de lo que no usa
- Cumplimos ISP al 100%
"""


# ============================================================
# ✔️ IMPLEMENTACIONES LIMPIAS
# ============================================================

class RepositorioUsuariosSQL(UsuarioReader, UsuarioWriter, UsuarioDeleter):
    def crear(self, data: dict) -> None:
        print("Usuario creado en SQL")

    def obtener_por_id(self, user_id: int) -> dict:
        return {"id": user_id, "fuente": "SQL"}

    def eliminar(self, user_id: int) -> None:
        print("Usuario eliminado en SQL")


class RepositorioUsuariosReadOnly(UsuarioReader):
    def obtener_por_id(self, user_id: int) -> dict:
        return {"id": user_id, "fuente": "READ_ONLY"}


"""
Observa:
- Cada clase implementa SOLO lo que necesita
- No hay métodos inútiles
- No hay excepciones artificiales
"""


# ============================================================
# 🔥 USO REAL EN SERVICIOS BACKEND
# ============================================================

def servicio_consultar_usuario(repo: UsuarioReader, user_id: int) -> dict:
    return repo.obtener_por_id(user_id)


def servicio_crear_usuario(repo: UsuarioWriter, data: dict) -> None:
    repo.crear(data)


# ✔️ Sustitución limpia
servicio_consultar_usuario(RepositorioUsuariosSQL(), 1)
servicio_consultar_usuario(RepositorioUsuariosReadOnly(), 2)

servicio_crear_usuario(RepositorioUsuariosSQL(), {"name": "Juan"})


"""
Clave:
👉 Cada servicio depende SOLO de lo que necesita.
Esto es diseño profesional.
"""


# ============================================================
# 🧠 REGLAS MENTALES PARA APLICAR ISP
# ============================================================

"""
1️⃣ Si una interfaz crece demasiado → divídela
2️⃣ Si una clase implementa métodos vacíos → mala señal
3️⃣ Si un servicio usa solo 1 método → no le pases 5
4️⃣ Prefiere roles pequeños y claros
5️⃣ Interfaces = contratos, no cajones desastre
"""


# ============================================================
# 🎯 CONEXIÓN DIRECTA CON TU CAMINO (backend + IA)
# ============================================================

"""
ISP es CRÍTICO para:
- Microservicios
- Pipelines de datos
- Sistemas testeables
- Arquitecturas limpias

En ML / Data:
- Un componente puede leer features
- Otro puede transformarlas
- Otro persistir resultados

No mezcles responsabilidades.

Si dominas ISP:
➡️ Diseñas sistemas que escalan
➡️ Escribes código reutilizable
➡️ Piensas como ingeniero, no como estudiante

Esto ya es nivel profesional serio.
"""
