# bucles_for_while.py
"""
Bucles for y while en Backend Python – Uso Profesional

Este módulo cubre:
- Cuándo usar for y cuándo while
- Errores reales de backend con bucles
- Patrones profesionales
- Cómo evitar bucles infinitos y consumo innecesario
"""

# -------------------------------------------------
# 1. for vs while (decisión profesional)
# -------------------------------------------------
# for → cuando sabes QUÉ iteras
# while → cuando sabes CUÁNDO paras

# ❌ while por costumbre
i = 0
while i < 5:
    print(i)
    i += 1

# ✔️ for claro
for i in range(5):
    print(i)


# -------------------------------------------------
# 2. Iterar sobre colecciones
# -------------------------------------------------

usuarios = ["ana", "juan", "lucia"]

# ✔️ Correcto
for usuario in usuarios:
    print(usuario)

# ❌ Error común
# for i in range(len(usuarios)):
#     print(usuarios[i])


# -------------------------------------------------
# 3. Iterar con índice (solo si hace falta)
# -------------------------------------------------

for idx, usuario in enumerate(usuarios):
    print(idx, usuario)


# -------------------------------------------------
# 4. Bucles infinitos (error crítico)
# -------------------------------------------------

# ❌ Backend muerto
# while True:
#     procesar()

# ✔️ Control explícito
def procesar_eventos(max_eventos=10):
    procesados = 0
    while procesados < max_eventos:
        print("Procesando evento")
        procesados += 1


# -------------------------------------------------
# 5. break y continue (uso correcto)
# -------------------------------------------------

for i in range(10):
    if i == 5:
        break  # salir del bucle
    if i % 2 == 0:
        continue  # saltar iteración
    print(i)


# -------------------------------------------------
# 6. Evitar trabajo innecesario
# -------------------------------------------------

# ❌ Recorre todo aunque ya encontró
def buscar_malo(lista, objetivo):
    encontrado = False
    for x in lista:
        if x == objetivo:
            encontrado = True
    return encontrado

# ✔️ Profesional
def buscar_bueno(lista, objetivo):
    for x in lista:
        if x == objetivo:
            return True
    return False


# -------------------------------------------------
# 7. while en backend real
# -------------------------------------------------

# ✔️ Lectura hasta condición externa
def leer_stream(datos):
    i = 0
    while i < len(datos):
        print(datos[i])
        i += 1


# -------------------------------------------------
# 8. Bucles + IO (zona peligrosa)
# -------------------------------------------------

# ❌ IO dentro de loop grande
# for usuario in usuarios:
#     guardar_en_bd(usuario)

# ✔️ Batch
def guardar_lote(lote):
    print(f"Guardando {len(lote)} usuarios")

guardar_lote(usuarios)


# -------------------------------------------------
# 9. Anidamiento de bucles (alerta roja)
# -------------------------------------------------

# ❌ O(n²)
# for a in datos:
#     for b in datos:
#         procesar(a, b)

# ✔️ Replantear estructura
# usar sets, dicts o índices


# -------------------------------------------------
# 10. Bucles con else (poco conocido)
# -------------------------------------------------

for x in [1, 3, 5]:
    if x % 2 == 0:
        break
else:
    print("No se encontraron pares")


# -------------------------------------------------
# 11. Generadores > bucles pesados
# -------------------------------------------------

def generar():
    for i in range(1_000_000):
        yield i

for valor in generar():
    pass  # consumo controlado


# -------------------------------------------------
# 12. Error típico de principiante
# -------------------------------------------------
# ❌ while sin límite
# ❌ for sobre range(len())
# ❌ break sin control
# ❌ bucles con lógica compleja dentro


# -------------------------------------------------
# 13. Checklist mental backend
# -------------------------------------------------
# ✔️ ¿Sé cuándo termina?
# ✔️ ¿Puedo salir antes?
# ✔️ ¿Estoy haciendo IO aquí?
# ✔️ ¿Hay loops anidados?
# ✔️ ¿Puedo usar estructuras mejores?


# -------------------------------------------------
# 14. Regla de oro
# -------------------------------------------------
"""
Un bucle innecesario no da error,
da facturas más caras.
"""
