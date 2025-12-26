# objetos_inmutables.py
# Seguridad y predictibilidad en clases inmutables

# ------------------------------------------------------------
# En sistemas reales (backend, data, APIs) es fundamental
# que ciertos objetos no puedan ser modificados una vez creados.
# Esto evita bugs difíciles de rastrear, problemas de concurrencia
# y hace tu código más predecible y seguro.
# ------------------------------------------------------------

# EJEMPLO 1: Clase tradicional mutable (problema)
class Usuario:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

usuario = Usuario("Ana", "ana@example.com")
usuario.email = "hacker@example.com"  # mutable, puede causar problemas
print(usuario.email)  # hacker@example.com

# ------------------------------------------------------------
# EJEMPLO 2: Haciendo la clase inmutable con propiedades privadas
class UsuarioInmutable:
    def __init__(self, nombre, email):
        self.__nombre = nombre
        self.__email = email

    @property
    def nombre(self):
        return self.__nombre

    @property
    def email(self):
        return self.__email

usuario_inmutable = UsuarioInmutable("Ana", "ana@example.com")
print(usuario_inmutable.email)  # ana@example.com
# usuario_inmutable.email = "hacker@example.com"  # ❌ Error: no se puede asignar

# ------------------------------------------------------------
# EJEMPLO 3: Usando dataclasses con frozen=True (Python moderno)
from dataclasses import dataclass

@dataclass(frozen=True)
class UsuarioDTO:
    nombre: str
    email: str

usuario_dto = UsuarioDTO("Ana", "ana@example.com")
print(usuario_dto.email)  # ana@example.com
# usuario_dto.email = "hacker@example.com"  # ❌ Error: objeto inmutable

# ------------------------------------------------------------
# CONSEJOS PRÁCTICOS PARA BACKEND/DATOS:
# 1. Usa objetos inmutables para IDs, DTOs, configuraciones.
# 2. Evita exponer referencias directas a listas/dicts internas.
# 3. Si necesitas "cambiar" un objeto, crea uno nuevo.
# 4. Facilita testing: objetos inmutables son más predecibles.
# 5. En pipelines de datos, evita efectos colaterales mutables.

# ------------------------------------------------------------
# EJEMPLO PRÁCTICO DE USO:
# Supongamos un microservicio que procesa usuarios y envía correos.

from typing import List

@dataclass(frozen=True)
class UsuarioEmail:
    nombre: str
    email: str

def enviar_mails(usuarios: List[UsuarioEmail]):
    for u in usuarios:
        # seguro: los datos no cambiarán dentro de la función
        print(f"Enviando correo a {u.email}")

usuarios = [UsuarioEmail("Ana", "ana@example.com"),
            UsuarioEmail("Luis", "luis@example.com")]

enviar_mails(usuarios)
