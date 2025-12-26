# lsp_liskov.py

"""
Liskov Substitution Principle (LSP)
----------------------------------
“Las clases derivadas deben poder sustituir a sus clases base
SIN romper el comportamiento esperado del programa.”

Traducción clara y sin humo:
👉 Si una función espera una clase base,
   DEBE funcionar igual con cualquier subclase.

Si al usar una subclase:
- rompe lógica
- lanza errores inesperados
- obliga a hacer if isinstance(...)
entonces has VIOLADO LSP.

Esto es uno de los errores más comunes incluso en gente con experiencia.
"""

# ============================================================
# ❌ MAL EJEMPLO: violación clásica de LSP
# ============================================================

class Ave:
    def volar(self) -> None:
        print("El ave vuela")


class Pinguino(Ave):
    def volar(self) -> None:
        raise Exception("Los pingüinos no pueden volar")


def hacer_volar(ave: Ave) -> None:
    ave.volar()


"""
PROBLEMA:
- hacer_volar espera un Ave
- Pinguino es un Ave
- pero rompe el contrato → CRASHEA

Esto VIOLA LSP.
La herencia está MAL planteada.
"""

# hacer_volar(Pinguino())  # 💥 BOOM


# ============================================================
# 💥 POR QUÉ ESTO ES GRAVE EN BACKEND
# ============================================================

"""
En backend real esto se traduce en:
- Endpoints que fallan según el tipo concreto
- Servicios que necesitan ifs defensivos
- Bugs en producción imposibles de prever
- Tests frágiles

Si necesitas preguntar:
    if isinstance(obj, SubClase):
        ...
YA has roto LSP.
"""


# ============================================================
# ✅ SOLUCIÓN CORRECTA: abstraer bien el comportamiento
# ============================================================

from abc import ABC, abstractmethod


class Ave(ABC):
    @abstractmethod
    def moverse(self) -> None:
        pass


class AveVoladora(Ave):
    def moverse(self) -> None:
        print("El ave vuela")


class AveNoVoladora(Ave):
    def moverse(self) -> None:
        print("El ave camina")


class Aguila(AveVoladora):
    pass


class Pinguino(AveNoVoladora):
    pass


def mover_ave(ave: Ave) -> None:
    ave.moverse()


# ✔️ TODAS las subclases funcionan correctamente
mover_ave(Aguila())
mover_ave(Pinguino())


"""
Ahora:
- Ninguna subclase rompe expectativas
- No hay excepciones sorpresa
- El contrato es claro
- LSP se cumple
"""


# ============================================================
# 🔥 EJEMPLO REALISTA EN TU CONTEXTO: BACKEND
# ============================================================

class RepositorioUsuarios(ABC):
    @abstractmethod
    def obtener_por_id(self, user_id: int) -> dict:
        pass


class RepositorioUsuariosSQL(RepositorioUsuarios):
    def obtener_por_id(self, user_id: int) -> dict:
        return {"id": user_id, "fuente": "SQL"}


class RepositorioUsuariosMock(RepositorioUsuarios):
    def obtener_por_id(self, user_id: int) -> dict:
        return {"id": user_id, "fuente": "MOCK"}


def servicio_usuario(repo: RepositorioUsuarios, user_id: int) -> dict:
    """
    Este servicio NO sabe ni le importa
    qué implementación concreta recibe.
    """
    return repo.obtener_por_id(user_id)


# ✔️ Sustitución perfecta
print(servicio_usuario(RepositorioUsuariosSQL(), 1))
print(servicio_usuario(RepositorioUsuariosMock(), 1))


"""
Esto es LSP aplicado a backend profesional:
- Testeable
- Desacoplado
- Robusto
"""


# ============================================================
# ❌ EJEMPLO REAL DE VIOLACIÓN EN BACKEND
# ============================================================

class RepositorioUsuariosRoto(RepositorioUsuarios):
    def obtener_por_id(self, user_id: int) -> dict:
        raise NotImplementedError("No implementado todavía")


"""
Esto rompe LSP porque:
- La clase promete un comportamiento
- Pero no lo cumple
- Cualquier servicio que la use puede romper

Una subclase NUNCA debería:
- Lanzar excepciones donde la base no lo espera
- Reducir funcionalidades
- Cambiar tipos de retorno
"""


# ============================================================
# 🧠 REGLAS MENTALES PARA NO ROMPER LSP
# ============================================================

"""
1️⃣ Una subclase debe poder usarse SIN QUE NADIE LO NOTE
2️⃣ No lances excepciones nuevas inesperadas
3️⃣ No cambies el significado del método
4️⃣ No devuelvas tipos incompatibles
5️⃣ Si no puedes cumplir el contrato → NO heredes

Regla de oro:
❗ Si dudas si una clase es realmente "un tipo de" otra → probablemente NO lo sea.
"""


# ============================================================
# 🎯 CONEXIÓN DIRECTA CON TU CAMINO (backend + IA)
# ============================================================

"""
LSP es clave para:
- Arquitecturas limpias
- Pipelines de datos intercambiables
- Modelos y servicios extensibles
- Código que escala sin romperse

Dominar LSP te pone muy por encima
del programador medio que solo “usa clases”.

Esto ya es mentalidad profesional.
"""
