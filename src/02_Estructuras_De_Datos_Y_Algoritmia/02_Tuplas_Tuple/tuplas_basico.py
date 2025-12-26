# tuplas_basico.py
"""
TUPLAS EN PYTHON — FUNDAMENTOS PROFESIONALES
===========================================

Una tupla es:
- Una colección ORDENADA
- INMUTABLE
- Más ligera y predecible que una lista

En backend y data se usan para:
- Garantizar que algo NO se modifica
- Representar registros fijos
- Claves y contratos de datos
"""

# ------------------------------------------------------------
# 1. CREACIÓN DE TUPLAS
# ------------------------------------------------------------

t1 = (1, 2, 3)
t2 = 1, 2, 3        # paréntesis opcionales
t3 = (1,)           # tupla de un solo elemento (OJO a la coma)

print(type(t1))
print(type(t2))
print(type(t3))


# ------------------------------------------------------------
# 2. INMUTABILIDAD (PUNTO CLAVE)
# ------------------------------------------------------------

coords = (10, 20)

# coords[0] = 99   # ❌ ERROR: TypeError

"""
La inmutabilidad:
✔ Evita bugs
✔ Hace el código más predecible
✔ Permite usar tuplas como claves
"""


# ------------------------------------------------------------
# 3. TUPLAS VS LISTAS (USO CORRECTO)
# ------------------------------------------------------------

"""
Usa TUPLA cuando:
✔ El conjunto de datos no debe cambiar
✔ Representa un registro fijo
✔ Es un valor de retorno múltiple

Usa LISTA cuando:
✔ Necesitas modificar
✔ Agregar / eliminar elementos
"""

usuario = ("id_123", "Juan", 29)   # tupla → registro
carrito = ["producto1", "producto2"]  # lista → mutable


# ------------------------------------------------------------
# 4. DESEMPAQUETADO DE TUPLAS
# ------------------------------------------------------------

persona = ("Ana", 30, "Madrid")

nombre, edad, ciudad = persona

print(nombre)
print(edad)
print(ciudad)


# ------------------------------------------------------------
# 5. DESEMPAQUETADO PARCIAL Y *
# ------------------------------------------------------------

datos = (1, 2, 3, 4, 5)

a, b, *resto = datos

print(a, b)
print(resto)


# ------------------------------------------------------------
# 6. RETORNO MÚLTIPLE DE FUNCIONES
# ------------------------------------------------------------

def dividir(a, b):
    return a // b, a % b

cociente, resto = dividir(10, 3)

print(cociente, resto)

"""
Patrón MUY usado en backend.
No se devuelven listas aquí.
"""


# ------------------------------------------------------------
# 7. TUPLAS PUEDEN CONTENER MUTABLES (OJO)
# ------------------------------------------------------------

t = (1, [2, 3])

t[1].append(4)

print(t)

"""
❗ La tupla es inmutable,
pero sus elementos pueden NO serlo.
"""


# ------------------------------------------------------------
# 8. ITERACIÓN Y ACCESO
# ------------------------------------------------------------

t = ("a", "b", "c")

print(t[0])

for item in t:
    print(item)


# ------------------------------------------------------------
# 9. USO COMO CONSTANTES
# ------------------------------------------------------------

ESTADOS_VALIDOS = ("CREADO", "PAGADO", "ENVIADO")

estado = "PAGADO"

if estado in ESTADOS_VALIDOS:
    print("Estado correcto")


# ------------------------------------------------------------
# 10. COSTE Y RENDIMIENTO
# ------------------------------------------------------------

"""
✔ Menos memoria que una lista
✔ Iteración igual de rápida
✔ Acceso por índice O(1)

Pero:
❌ No modificables
"""


# ------------------------------------------------------------
# 11. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Olvidar la coma en tupla de 1 elemento
❌ Usar lista cuando debería ser tupla
❌ Pensar que todo dentro es inmutable
"""


print("Tuplas básicas dominadas")
