# listas_en_backend.py
"""
Listas en Backend Python – Uso Profesional

Este módulo cubre:
- Qué es realmente una lista en Python (a nivel práctico)
- Cuándo usar listas y cuándo NO
- Costes de operaciones (impacto en rendimiento)
- Errores reales de backend con listas
- Patrones profesionales
"""

# -------------------------------------------------
# 1. Qué es una lista en backend (realidad)
# -------------------------------------------------
# Una lista en Python es:
# - Estructura ordenada
# - Mutable
# - Acceso por índice O(1)
# - Inserciones/eliminaciones NO siempre baratas

usuarios = ["ana", "juan", "lucia"]


# -------------------------------------------------
# 2. Casos reales de uso en backend
# -------------------------------------------------

# ✔️ Colecciones pequeñas en memoria
# ✔️ Resultados de una query SQL
# ✔️ Lotes de datos (batch)
# ✔️ Serialización JSON (arrays)

response_api = [
    {"id": 1, "email": "a@test.com"},
    {"id": 2, "email": "b@test.com"},
]


# -------------------------------------------------
# 3. Operaciones comunes y su coste
# -------------------------------------------------

lista = [1, 2, 3, 4, 5]

lista.append(6)        # ✔️ O(1)
lista.pop()            # ✔️ O(1)
lista[0]               # ✔️ O(1)

lista.insert(0, 99)    # ❌ O(n)
lista.pop(0)           # ❌ O(n)
99 in lista             # ❌ O(n)

# ⚠️ En backend con grandes volúmenes esto IMPORTA


# -------------------------------------------------
# 4. Iterar correctamente
# -------------------------------------------------

# ❌ Estilo estudiante
for i in range(len(lista)):
    print(lista[i])

# ✔️ Estilo profesional
for valor in lista:
    print(valor)

# ✔️ Con índice cuando es necesario
for idx, valor in enumerate(lista):
    print(idx, valor)


# -------------------------------------------------
# 5. Filtrado profesional
# -------------------------------------------------

usuarios = [
    {"id": 1, "activo": True},
    {"id": 2, "activo": False},
    {"id": 3, "activo": True},
]

# ❌ Imperativo largo
activos = []
for u in usuarios:
    if u["activo"]:
        activos.append(u)

# ✔️ Backend limpio
activos = [u for u in usuarios if u["activo"]]


# -------------------------------------------------
# 6. Copias: superficial vs referencia
# -------------------------------------------------

a = [1, 2, 3]
b = a          # ❌ MISMA lista
c = a.copy()   # ✔️ copia superficial

a.append(4)

# b -> [1,2,3,4]
# c -> [1,2,3]


# -------------------------------------------------
# 7. Listas como buffers (caso real)
# -------------------------------------------------

def procesar_en_lotes(datos, tamaño_lote=100):
    buffer = []
    for item in datos:
        buffer.append(item)
        if len(buffer) == tamaño_lote:
            enviar_a_bd(buffer)
            buffer.clear()

    if buffer:
        enviar_a_bd(buffer)

def enviar_a_bd(lote):
    # simulación
    print(f"Enviando lote de {len(lote)} registros")


# -------------------------------------------------
# 8. Errores comunes en backend
# -------------------------------------------------

# ❌ Modificar lista mientras iteras
datos = [1, 2, 3, 4]

# for x in datos:
#     if x % 2 == 0:
#         datos.remove(x)  # BUG

# ✔️ Forma correcta
datos = [x for x in datos if x % 2 != 0]


# -------------------------------------------------
# 9. Listas NO son sets ni dicts
# -------------------------------------------------

ids = [1, 2, 3, 4, 5]

# ❌ Mala elección
if 3 in ids:  # O(n)
    pass

# ✔️ Si necesitas pertenencia rápida
ids_set = set(ids)
if 3 in ids_set:  # O(1)
    pass


# -------------------------------------------------
# 10. Listas y memoria
# -------------------------------------------------

# ⚠️ Cargar millones de registros en listas
# puede romper el servidor

# ✔️ Alternativa: generadores
def leer_datos():
    for i in range(10_000_000):
        yield i


# -------------------------------------------------
# 11. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Usa listas para colecciones ordenadas
# ✔️ Evita insert/pop al inicio
# ✔️ No mezcles tipos sin razón
# ✔️ Copia explícitamente
# ✔️ Piensa en volumen de datos
# ✔️ Cambia a set/dict cuando el caso lo pida


# -------------------------------------------------
# 12. Regla de oro backend
# -------------------------------------------------
"""
Si no sabes cuántos elementos vas a tener,
o si va a crecer mucho,
PIENSA DOS VECES antes de usar una lista.
"""
