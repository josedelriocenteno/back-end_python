# parametros_y_retorno.py
"""
Parámetros y Retorno en Funciones Python – Nivel Profesional

Este módulo cubre:
- Cómo definir parámetros claros
- Cómo retornar datos consistentes
- Patrones profesionales de backend
- Errores comunes que generan bugs silenciosos
"""

# -------------------------------------------------
# 1. Parámetros obligatorios
# -------------------------------------------------

def sumar(a: int, b: int) -> int:
    """
    Suma dos números enteros.
    """
    return a + b

resultado = sumar(3, 5)
print(resultado)  # 8


# -------------------------------------------------
# 2. Parámetros por defecto
# -------------------------------------------------

# ❌ Mutable como default → error clásico
def agregar_item(lista=[]):
    lista.append(1)
    return lista

# ✔️ Seguro
def agregar_item_seguro(lista=None):
    if lista is None:
        lista = []
    lista.append(1)
    return lista


# -------------------------------------------------
# 3. Parámetros nombrados (kwargs)
# -------------------------------------------------

def crear_usuario(nombre: str, edad: int, rol: str = "user"):
    return {"nombre": nombre, "edad": edad, "rol": rol}

usuario = crear_usuario(nombre="Ana", edad=25)
usuario_admin = crear_usuario(nombre="Juan", edad=30, rol="admin")


# -------------------------------------------------
# 4. Parámetros variables (*args y **kwargs)
# -------------------------------------------------

def sumar_todos(*numeros: int) -> int:
    return sum(numeros)

print(sumar_todos(1, 2, 3, 4))  # 10

def crear_usuario_completo(nombre, **info):
    usuario = {"nombre": nombre}
    usuario.update(info)
    return usuario

usuario = crear_usuario_completo("Ana", rol="admin", activo=True)


# -------------------------------------------------
# 5. Retorno claro y consistente
# -------------------------------------------------

# ❌ Malo: retorno inconsistente
def buscar_usuario(id):
    if id == 1:
        return {"nombre": "Ana"}
    # else nada → retorno None

# ✔️ Profesional: siempre retorna mismo tipo
def buscar_usuario_seguro(id: int) -> dict:
    usuarios = {1: {"nombre": "Ana"}}
    return usuarios.get(id, {})


# -------------------------------------------------
# 6. Tipado y hints
# -------------------------------------------------

from typing import List, Dict, Optional

def procesar_usuarios(usuarios: List[Dict[str, str]]) -> List[str]:
    return [u["nombre"] for u in usuarios if "nombre" in u]


# -------------------------------------------------
# 7. Retorno múltiple
# -------------------------------------------------

# ✔️ Útil para evitar mutabilidad global
def coordenadas() -> tuple[int, int]:
    x = 10
    y = 20
    return x, y

x, y = coordenadas()


# -------------------------------------------------
# 8. Errores comunes de juniors
# -------------------------------------------------
# ❌ Parámetros confusos o sin default
# ❌ Retorno inconsistente (a veces None)
# ❌ Mezclar tipos de retorno
# ❌ Mutable por defecto


# -------------------------------------------------
# 9. Checklist mental backend
# -------------------------------------------------
# ✔️ Parámetros claros y tipados?
# ✔️ Default seguro si aplica?
# ✔️ Retorno consistente y tipado?
# ✔️ Fácil de testear?
# ✔️ Evita mutabilidad global?


# -------------------------------------------------
# 10. Regla de oro
# -------------------------------------------------
"""
Un parámetro bien definido y un retorno consistente
evitan bugs silenciosos y facilitan el testing.
"""
