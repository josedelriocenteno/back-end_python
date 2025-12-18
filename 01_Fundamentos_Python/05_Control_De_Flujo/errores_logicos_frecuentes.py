# errores_logicos_frecuentes.py
"""
Errores Lógicos Frecuentes en Backend Python – Nivel Profesional

Este módulo cubre:
- Los fallos mentales que generan bugs silenciosos
- Patrón de pensamiento profesional
- Cómo evitarlos desde el día 1
"""

# -------------------------------------------------
# 1. Confundir asignación con comparación
# -------------------------------------------------

# ❌ Error clásico
x = 5
# if x = 10:  # SyntaxError, pero conceptualmente confuso

# ✔️ Correcto
if x == 10:
    print("x es 10")


# -------------------------------------------------
# 2. Comparaciones incompletas
# -------------------------------------------------

edad = 18

# ❌ Lógico incorrecto
# if edad > 18:
#     print("Adulto")
# else:
#     print("No adulto")  # 18 queda fuera

# ✔️ Correcto
if edad >= 18:
    print("Adulto")
else:
    print("No adulto")


# -------------------------------------------------
# 3. Orden de condiciones
# -------------------------------------------------

nota = 8

# ❌ Error lógico
# if nota >= 5:
#     print("Aprobado")
# elif nota >= 9:
#     print("Excelente")

# ✔️ Profesional
if nota >= 9:
    print("Excelente")
elif nota >= 5:
    print("Aprobado")
else:
    print("Suspenso")


# -------------------------------------------------
# 4. Confundir mutables e inmutables
# -------------------------------------------------

lista = [1, 2, 3]
tupla = (1, 2, 3)

# ❌ Cambiar accidentalmente lista compartida
def add_elemento(arr):
    arr.append(4)

add_elemento(lista)  # muta original
# add_elemento(tupla) → TypeError (seguro)


# -------------------------------------------------
# 5. Truthy/Falsy mal interpretado
# -------------------------------------------------

datos = []

# ❌ Junior hace esto
if datos:
    print("Hay datos")  # falso positivo si datos = None

# ✔️ Profesional
if datos is not None and len(datos) > 0:
    print("Hay datos")


# -------------------------------------------------
# 6. Comparar con None
# -------------------------------------------------

resultado = None

# ❌ Malo
# if resultado == None:

# ✔️ Profesional
if resultado is None:
    print("No hay resultado")


# -------------------------------------------------
# 7. Bucles mal controlados
# -------------------------------------------------

# ❌ Bucle infinito
# while True:
#     procesar()

# ✔️ Controlado
contador = 0
while contador < 5:
    print("Procesando")
    contador += 1


# -------------------------------------------------
# 8. Sobrescribir variables sin querer
# -------------------------------------------------

x = 10
# ...
x = x + 1  # cuidado, que no borres valor anterior sin querer

# ✔️ Mejor nombrar explícito
x_incrementado = x + 1


# -------------------------------------------------
# 9. Comparaciones de strings inconsistentes
# -------------------------------------------------

estado = "Activo"

# ❌ Error frecuente
# if estado == "activo":

# ✔️ Normalizar
if estado.lower() == "activo":
    print("Usuario activo")


# -------------------------------------------------
# 10. Mezclar lógica y efectos secundarios
# -------------------------------------------------

# ❌ Difícil de testear
for u in ["ana", "juan"]:
    print(u)  # efecto
    if len(u) > 3:
        print("Nombre largo")  # lógica mezclada

# ✔️ Profesional
def nombre_largo(nombre):
    return len(nombre) > 3

for u in ["ana", "juan"]:
    if nombre_largo(u):
        print(f"{u} tiene nombre largo")


# -------------------------------------------------
# 11. Comparaciones flotantes
# -------------------------------------------------

a = 0.1 + 0.2
b = 0.3

# ❌ == directo falla
if a == b:
    print("Iguales")  # NO se cumple

# ✔️ Forma correcta
if abs(a - b) < 1e-9:
    print("Prácticamente iguales")


# -------------------------------------------------
# 12. Checklist mental backend
# -------------------------------------------------
# ✔️ ¿Comparaciones claras y completas?
# ✔️ ¿Mutabilidad controlada?
# ✔️ ¿Truthy/Falsy explícito?
# ✔️ ¿Bucle controlado?
# ✔️ ¿Variables bien nombradas?
# ✔️ ¿Efectos separados de lógica?


# -------------------------------------------------
# 13. Regla de oro
# -------------------------------------------------
"""
Un error lógico no da error de sintaxis,
da bugs silenciosos que matan sistemas.
"""
