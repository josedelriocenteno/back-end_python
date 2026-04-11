# definicion_y_llamadas.py
"""
Definición y Llamadas de Funciones en Backend Python – Nivel Profesional

Este módulo cubre:
- Cómo definir funciones correctamente
- Cómo llamarlas de manera segura y clara
- Errores comunes en producción
- Patrones profesionales y mantenibles
"""

# -------------------------------------------------
# 1. Definir funciones claras
# -------------------------------------------------

# ❌ Junior
def calcular(a, b):
    return a + b  # qué hace? qué unidades?

# ✔️ Profesional
def sumar_dos_numeros(a: int, b: int) -> int:
    """
    Suma dos números enteros.

    Args:
        a (int): primer número
        b (int): segundo número

    Returns:
        int: resultado de a + b
    """
    return a + b


# -------------------------------------------------
# 2. Llamadas claras y legibles
# -------------------------------------------------

resultado = sumar_dos_numeros(3, 5)
print(resultado)  # 8

# ✔️ Evitar llamadas confusas
# ❌ sumar_dos_numeros(3, b=5, a=7)  # no hagas rebotes


# -------------------------------------------------
# 3. Funciones con efectos secundarios
# -------------------------------------------------

# ❌ Mal: print dentro de lógica
def procesar_usuario(usuario):
    print(f"Procesando {usuario}")  # mezcla de lógica y side effect

# ✔️ Profesional
def procesar_usuario_backend(usuario):
    """
    Procesa un usuario en backend.
    Retorna datos procesados, no imprime.
    """
    return {"usuario": usuario, "procesado": True}


# -------------------------------------------------
# 4. Funciones puras vs impuras
# -------------------------------------------------

# Puras: salida depende solo de inputs, sin efectos secundarios
def multiplicar(a: int, b: int) -> int:
    return a * b

# Impuras: modifican estado externo o hacen IO
contador_global = 0
def incrementar_contador():
    global contador_global
    contador_global += 1  # impuro


# -------------------------------------------------
# 5. Valores por defecto
# -------------------------------------------------

# ❌ Mutable como default → error clásico
def agregar_elemento(lista=[]):
    lista.append(1)
    return lista

# ✔️ Seguro
def agregar_elemento_seguro(lista=None):
    if lista is None:
        lista = []
    lista.append(1)
    return lista


# -------------------------------------------------
# 6. Tipado y hints
# -------------------------------------------------

# ✔️ Mejora lectura y detecta errores temprano
from typing import List, Dict

def procesar_usuarios(usuarios: List[Dict[str, str]]) -> List[str]:
    return [u["nombre"] for u in usuarios if "nombre" in u]


# -------------------------------------------------
# 7. Llamadas con kwargs y args
# -------------------------------------------------

def crear_usuario(nombre, **kwargs):
    usuario = {"nombre": nombre}
    usuario.update(kwargs)
    return usuario

usuario = crear_usuario("Ana", rol="admin", activo=True)


# -------------------------------------------------
# 8. Funciones anidadas y closures
# -------------------------------------------------

def generador_de_incremento(incremento):
    def incrementar(x):
        return x + incremento
    return incrementar

sumar_5 = generador_de_incremento(5)
print(sumar_5(10))  # 15


# -------------------------------------------------
# 9. Errores frecuentes de juniors
# -------------------------------------------------
# ❌ Mezclar print con retorno
# ❌ Default mutable
# ❌ No usar hints
# ❌ Llamadas con kwargs confusas
# ❌ Funciones largas (>50 líneas)


# -------------------------------------------------
# 10. Checklist mental backend
# -------------------------------------------------
# ✔️ Función corta y clara?
# ✔️ Tipos claros?
# ✔️ Efectos separados de retorno?
# ✔️ Nombre que dice qué hace?
# ✔️ Probable de testear?


# -------------------------------------------------
# 11. Regla de oro
# -------------------------------------------------
"""
Una función profesional es como un ladrillo bien cortado:
- clara
- sólida
- fácil de unir con otras funciones
"""
