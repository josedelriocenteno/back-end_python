# mutabilidad_y_memoria.py
"""
MUTABILIDAD Y MEMORIA EN PYTHON
==============================

Este archivo explica una de las cosas MÁS IMPORTANTES de Python
para backend y data engineering.

Si NO entiendes esto:
- Introducirás bugs invisibles
- Romperás datos sin darte cuenta
- Crearás efectos secundarios peligrosos
"""

# ------------------------------------------------------------
# 1. MEMORIA, VARIABLES Y REFERENCIAS
# ------------------------------------------------------------

"""
En Python:
- Las variables NO contienen valores
- Las variables APUNTAN a objetos en memoria

Piensa en variables como etiquetas (labels), no como cajas.
"""

a = 10
b = a

# a y b apuntan al MISMO objeto 10 (inmutable)

print(a, b)          # 10 10
print(id(a), id(b))  # mismo id (misma referencia)


# ------------------------------------------------------------
# 2. MUTABLE VS INMUTABLE (CONCEPTO CLAVE)
# ------------------------------------------------------------

"""
INMUTABLE:
- No se puede modificar el objeto
- Se crea uno nuevo si "cambia"

MUTABLE:
- El objeto se puede modificar en memoria
"""

# Inmutables comunes:
# int, float, bool, str, tuple, frozenset

# Mutables comunes:
# list, dict, set, bytearray


# ------------------------------------------------------------
# 3. EJEMPLO CON INMUTABLES
# ------------------------------------------------------------

x = 5
y = x

x = x + 1  # crea un NUEVO objeto

print(x)  # 6
print(y)  # 5

"""
Aquí NO hay efecto secundario:
- x apunta a un nuevo objeto
- y sigue apuntando al antiguo
"""


# ------------------------------------------------------------
# 4. EJEMPLO CON MUTABLES (PELIGRO REAL)
# ------------------------------------------------------------

lista_a = [1, 2, 3]
lista_b = lista_a  # NO es una copia

lista_a.append(4)

print(lista_a)  # [1, 2, 3, 4]
print(lista_b)  # [1, 2, 3, 4]

"""
lista_a y lista_b apuntan al MISMO objeto en memoria.

Esto es la fuente número 1 de bugs en Python.
"""


# ------------------------------------------------------------
# 5. REFERENCIAS EN FUNCIONES (BACKEND REAL)
# ------------------------------------------------------------

def agregar_elemento(lista):
    lista.append("X")

datos = ["A", "B"]
agregar_elemento(datos)

print(datos)  # ['A', 'B', 'X']

"""
La función NO recibió una copia.
Recibió una REFERENCIA.

Esto puede ser:
- Útil (performance)
- PELIGROSO (efectos secundarios)
"""


# ------------------------------------------------------------
# 6. COPIA SUPERFICIAL (SHALLOW COPY)
# ------------------------------------------------------------

import copy

original = [1, 2, 3]
copia1 = original.copy()
copia2 = list(original)
copia3 = copy.copy(original)

original.append(4)

print(original)  # [1, 2, 3, 4]
print(copia1)    # [1, 2, 3]

"""
Shallow copy:
- Copia el contenedor
- NO copia los objetos internos
"""


# ------------------------------------------------------------
# 7. EL GRAN PROBLEMA: ESTRUCTURAS ANIDADAS
# ------------------------------------------------------------

original = [[1, 2], [3, 4]]
copia = original.copy()

original[0].append(99)

print(original)  # [[1, 2, 99], [3, 4]]
print(copia)     # [[1, 2, 99], [3, 4]]

"""
La lista externa es nueva,
pero las listas internas siguen compartidas.
"""


# ------------------------------------------------------------
# 8. COPIA PROFUNDA (DEEP COPY)
# ------------------------------------------------------------

deep = copy.deepcopy(original)

original[1].append(88)

print(original)  # [[1, 2, 99], [3, 4, 88]]
print(deep)      # [[1, 2, 99], [3, 4]]

"""
Deep copy:
- Copia todo recursivamente
- Más segura
- Más costosa
"""


# ------------------------------------------------------------
# 9. CUÁNDO USAR CADA TIPO DE COPIA
# ------------------------------------------------------------

"""
Shallow copy:
- Datos simples
- Rendimiento crítico
- Sabes lo que haces

Deep copy:
- Datos anidados
- Seguridad > rendimiento
- Evitar efectos secundarios
"""


# ------------------------------------------------------------
# 10. MUTABILIDAD EN DICCIONARIOS
# ------------------------------------------------------------

config = {
    "db": {"host": "localhost", "port": 5432}
}

config_copy = config.copy()
config["db"]["port"] = 9999

print(config_copy["db"]["port"])  # 9999 ❌

"""
BUG REAL DE BACKEND:
Modificar configuración compartida sin querer
"""


# ------------------------------------------------------------
# 11. PATRÓN DEFENSIVO PROFESIONAL
# ------------------------------------------------------------

def procesar_config(cfg):
    cfg = copy.deepcopy(cfg)  # defensa explícita
    cfg["db"]["port"] = 1111
    return cfg

"""
En backend serio:
- O documentas mutabilidad
- O proteges con copia
"""


# ------------------------------------------------------------
# 12. MUTABILIDAD Y DEFAULT ARGUMENTS (TRAMPA CLÁSICA)
# ------------------------------------------------------------

def agregar_item(item, lista=[]):
    lista.append(item)
    return lista

print(agregar_item(1))
print(agregar_item(2))
print(agregar_item(3))

"""
Salida:
[1]
[1, 2]
[1, 2, 3]

ERROR CRÍTICO.
El default se evalúa UNA VEZ.
"""

# Solución correcta
def agregar_item_seguro(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista


# ------------------------------------------------------------
# 13. REGLAS DE ORO (MEMORIZA ESTO)
# ------------------------------------------------------------

"""
1. Asignar NO copia
2. Mutable + referencia = efecto secundario
3. Shallow copy NO copia lo interno
4. Deep copy es seguro pero caro
5. Nunca uses mutables como default arguments
6. En backend, documenta o protege mutabilidad
"""


# ------------------------------------------------------------
# 14. MENSAJE FINAL
# ------------------------------------------------------------

"""
Si entiendes mutabilidad y memoria:
- Entiendes Python de verdad
- Escribes código predecible
- Evitas bugs silenciosos
"""

print("Mutabilidad entendida = bugs evitados")
