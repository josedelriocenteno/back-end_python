"""
alternativas_pickle.py
======================

Este archivo muestra ALTERNATIVAS REALES y PROFESIONALES a pickle.

IMPORTANTE CONTEXTO
-------------------
pickle permite serializar objetos Python completos, pero:
- Ejecuta código al deserializar
- Es inseguro con datos externos
- No es portable entre lenguajes
- Puede romperse entre versiones

Por eso, en sistemas reales (backend, data, ML, producción),
pickle se evita SIEMPRE que sea posible.

Aquí veremos alternativas SEGURAS y cuándo usar cada una.

Regla clave:
"Serializa DATOS, no COMPORTAMIENTO"
"""

# ============================================================
# 1. JSON – ALTERNATIVA BASE Y UNIVERSAL
# ============================================================

"""
JSON es el formato más común para persistencia simple.

VENTAJAS:
- Seguro (no ejecuta código)
- Legible por humanos
- Portable entre lenguajes
- Estándar en APIs y configuración

LIMITACIONES IMPORTANTES:
JSON solo soporta tipos básicos:
- dict
- list
- str
- int / float
- bool
- None

NO soporta:
- Clases
- Funciones
- Objetos complejos
"""

import json


def guardar_json_basico():
    """
    Ejemplo básico de persistencia con JSON.

    Este es el NIVEL 1: guardar datos simples.
    """
    datos = {
        "usuario": "juan",
        "edad": 20,
        "activo": True,
        "roles": ["admin", "editor"]
    }

    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)


def leer_json_basico():
    """
    Lectura del JSON guardado previamente.
    """
    with open("datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos


# ============================================================
# 2. OBJETOS PYTHON → JSON (PATRÓN PROFESIONAL)
# ============================================================

"""
Aquí viene el salto importante.

JSON NO puede guardar objetos directamente.
La solución profesional es:
- Convertir el objeto a datos simples (dict)
- Guardar esos datos
- Reconstruir el objeto manualmente

Esto es diseño explícito y seguro.
"""


class Usuario:
    """
    Clase de ejemplo.

    Observa que:
    - NO intentamos serializar la clase
    - Solo serializamos sus DATOS
    """

    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad

    def to_dict(self) -> dict:
        """
        Convierte el objeto a un diccionario JSON-compatible.
        """
        return {
            "nombre": self.nombre,
            "edad": self.edad
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """
        Reconstruye el objeto desde datos persistidos.
        """
        return cls(
            nombre=data["nombre"],
            edad=data["edad"]
        )


def guardar_usuario(usuario: Usuario):
    """
    Guarda un objeto Usuario usando JSON de forma segura.
    """
    with open("usuario.json", "w", encoding="utf-8") as archivo:
        json.dump(usuario.to_dict(), archivo, indent=4)


def leer_usuario() -> Usuario:
    """
    Recupera un Usuario desde JSON.
    """
    with open("usuario.json", "r", encoding="utf-8") as archivo:
        data = json.load(archivo)

    return Usuario.from_dict(data)


# ============================================================
# 3. MSGPACK – JSON BINARIO (ALTO RENDIMIENTO)
# ============================================================

"""
MsgPack es similar a JSON pero en formato binario.

CUÁNDO USAR MSGPACK:
- Necesitas menos tamaño en disco
- Necesitas más velocidad
- Cache
- Comunicación entre servicios

SIGUE SIENDO SEGURO:
- No ejecuta código
- Solo datos
"""

try:
    import msgpack
except ImportError:
    msgpack = None
    # MsgPack no es parte de la librería estándar


def guardar_msgpack(datos: dict):
    """
    Guarda datos usando MsgPack.
    """
    if msgpack is None:
        raise RuntimeError("msgpack no está instalado")

    with open("datos.msgpack", "wb") as archivo:
        archivo.write(msgpack.packb(datos))


def leer_msgpack() -> dict:
    """
    Lee datos desde un archivo MsgPack.
    """
    if msgpack is None:
        raise RuntimeError("msgpack no está instalado")

    with open("datos.msgpack", "rb") as archivo:
        return msgpack.unpackb(archivo.read(), raw=False)


# ============================================================
# 4. COMPARACIÓN MENTAL (RESUMEN OPERATIVO)
# ============================================================

"""
JSON:
- Legible
- Estándar
- Ideal para backend y config

MsgPack:
- Más rápido
- Más compacto
- Ideal para sistemas internos y cache

Pickle:
- Inseguro
- No portable
- Solo aceptable en entornos 100% controlados
"""


# ============================================================
# 5. QUÉ NO HACER (ANTIPATRONES)
# ============================================================

"""
❌ NO serializar objetos directamente con pickle "por comodidad"
❌ NO cargar pickles de fuentes externas
❌ NO usar pickle como formato de intercambio
❌ NO confiar en pickle para persistencia a largo plazo
"""


# ============================================================
# 6. PATRÓN PROFESIONAL DEFINITIVO
# ============================================================

"""
PATRÓN CORRECTO:

1. Objeto → dict
2. dict → JSON / MsgPack
3. Al leer: dict → objeto

Esto es:
- Seguro
- Mantenible
- Explícito
- Profesional
"""


if __name__ == "__main__":
    # Demostración mínima controlada

    usuario = Usuario("Ana", 25)
    guardar_usuario(usuario)

    usuario_recuperado = leer_usuario()
    print(usuario_recuperado.nombre, usuario_recuperado.edad)
