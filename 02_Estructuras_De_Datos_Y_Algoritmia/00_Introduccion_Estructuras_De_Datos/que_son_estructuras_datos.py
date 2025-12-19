# que_son_estructuras_datos.py
"""
INTRODUCCIÓN A LAS ESTRUCTURAS DE DATOS
======================================

Este archivo NO es para memorizar.
Es para ENTENDER cómo piensa un backend/data engineer profesional.

Objetivo:
- Entender qué es una estructura de datos
- Por qué existen
- Qué problema resuelven
- Por qué elegir mal una estructura destruye rendimiento, escalabilidad y dinero
"""

# ------------------------------------------------------------
# 1. ¿QUÉ ES UNA ESTRUCTURA DE DATOS?
# ------------------------------------------------------------

"""
Una estructura de datos es una forma organizada de almacenar, acceder
y modificar información en memoria.

No es "una lista", "un dict" o "un set".
Eso es la IMPLEMENTACIÓN.

La estructura es el CONCEPTO:
- Cómo se guardan los datos
- Cómo se accede a ellos
- Qué operaciones son eficientes
- Qué operaciones son caras
"""

# Ejemplo mental:
# "Tengo datos"  -> MAL
# "Tengo datos y necesito accederlos rápido por clave" -> dict
# "Tengo datos y necesito evitar duplicados" -> set
# "Tengo datos en orden y necesito recorrerlos" -> list


# ------------------------------------------------------------
# 2. ¿POR QUÉ EXISTEN LAS ESTRUCTURAS DE DATOS?
# ------------------------------------------------------------

"""
Porque el ordenador NO es mágico.

La memoria:
- Es finita
- Tiene costes de acceso
- Tiene jerarquías (CPU cache, RAM, disco)

Las estructuras de datos existen para:
- Reducir tiempo de ejecución
- Reducir consumo de memoria
- Hacer el código más simple y claro
"""

# Backend real:
# - APIs con miles de peticiones por segundo
# - Pipelines con millones de registros
# - Consultas que deben responder en milisegundos

# Elegir mal una estructura:
# ❌ API lenta
# ❌ Pipeline que no escala
# ❌ Costes cloud disparados


# ------------------------------------------------------------
# 3. OPERACIONES FUNDAMENTALES EN CUALQUIER ESTRUCTURA
# ------------------------------------------------------------

"""
Todas las estructuras de datos se evalúan por cómo resuelven
estas operaciones básicas:

1. Inserción      -> guardar un dato
2. Acceso         -> obtener un dato
3. Búsqueda       -> encontrar un dato
4. Eliminación    -> borrar un dato
5. Iteración      -> recorrer datos
"""

# Ejemplo conceptual:
datos = [1, 2, 3, 4, 5]

# Inserción
datos.append(6)

# Acceso
valor = datos[0]

# Búsqueda
existe = 3 in datos

# Eliminación
datos.remove(4)

# Iteración
for x in datos:
    pass


# ------------------------------------------------------------
# 4. COSTE COMPUTACIONAL (LA PARTE QUE LOS JUNIORS IGNORAN)
# ------------------------------------------------------------

"""
No todas las operaciones cuestan lo mismo.

Ejemplo:
- Acceder a un índice en una lista -> rápido
- Buscar un elemento en una lista -> lento si es grande

Aquí entra la COMPLEJIDAD COMPUTACIONAL (Big-O).
"""

# No medimos en segundos exactos, medimos en ESCALABILIDAD.

# O(1)  -> constante (no importa el tamaño)
# O(n)  -> lineal (crece con el tamaño)
# O(n²) -> explosivo (peligro real)

# Backend rule:
# Si algo está en un endpoint o pipeline crítico,
# O(n²) es casi siempre INACEPTABLE.


# ------------------------------------------------------------
# 5. EJEMPLO REAL: LISTA VS DICCIONARIO
# ------------------------------------------------------------

usuarios_lista = [
    {"id": 1, "nombre": "Alice"},
    {"id": 2, "nombre": "Bob"},
    {"id": 3, "nombre": "Charlie"},
]

# Buscar usuario por id en lista (O(n))
def buscar_usuario_lista(user_id):
    for u in usuarios_lista:
        if u["id"] == user_id:
            return u
    return None

# Diccionario (O(1))
usuarios_dict = {
    1: {"id": 1, "nombre": "Alice"},
    2: {"id": 2, "nombre": "Bob"},
    3: {"id": 3, "nombre": "Charlie"},
}

def buscar_usuario_dict(user_id):
    return usuarios_dict.get(user_id)

"""
Ambos funcionan.
Pero uno escala y el otro no.

Esto es ingeniería, no magia.
"""


# ------------------------------------------------------------
# 6. ESTRUCTURAS DE DATOS ≠ SINTAXIS
# ------------------------------------------------------------

"""
ERROR CLÁSICO DE PRINCIPIANTE:

Pensar:
- "Uso list porque es más fácil"
- "Uso dict porque me dijeron que es rápido"

FORMA CORRECTA:
- ¿Qué operación es la más frecuente?
- ¿Acceso por índice?
- ¿Búsqueda?
- ¿Inserción?
- ¿Orden?
"""

# La estructura se elige POR EL PROBLEMA,
# no por comodidad.


# ------------------------------------------------------------
# 7. BACKEND Y DATA: POR QUÉ ESTO ES CRÍTICO
# ------------------------------------------------------------

"""
En backend y data engineering:

- Cada petición mal optimizada se multiplica por miles
- Cada pipeline ineficiente quema CPU y dinero
- Cada estructura incorrecta genera latencia

Un buen backend engineer:
- Piensa en estructuras antes de escribir código
- Conoce los costes sin mirar documentación
- Optimiza diseño, no micro-detalles
"""


# ------------------------------------------------------------
# 8. REGLAS DE ORO
# ------------------------------------------------------------

"""
1. Datos pequeños -> casi cualquier estructura sirve
2. Datos grandes -> la estructura importa MUCHO
3. Búsqueda frecuente -> dict / set
4. Orden + recorrido -> list
5. Unicidad -> set
6. Acceso por clave -> dict
7. Colas/pilas -> deque / list (según caso)
"""

# Si no sabes qué estructura usar:
# - Estudia el patrón de acceso
# - Piensa en Big-O
# - Piensa en escalabilidad futura


# ------------------------------------------------------------
# 9. MENSAJE FINAL
# ------------------------------------------------------------

"""
Las estructuras de datos no son teoría académica.
Son una herramienta diaria de backend y data engineers reales.

Dominar esto:
- Te hace escribir código más rápido
- Te hace escribir código más limpio
- Te hace escribir código que escala
"""

print("Las estructuras de datos son una decisión de ingeniería.")
