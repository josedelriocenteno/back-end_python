# if_elif_else.py
"""
CONDICIONALES IF / ELIF / ELSE
==============================

Objetivo:
- Escribir condicionales claras, legibles y mantenibles
- Evitar anidamientos innecesarios y condiciones redundantes
- Preparar código profesional para backend y pipelines de datos
"""

# =========================================================
# 1. Sintaxis básica
# =========================================================

x = 10

if x > 0:
    print("x es positivo")
elif x == 0:
    print("x es cero")
else:
    print("x es negativo")

# =========================================================
# 2. Buenas prácticas
# =========================================================

# a) Evitar anidamientos profundos
# ❌ Malo
if x > 0:
    if x < 20:
        print("x positivo y < 20")

# ✅ Mejor
if 0 < x < 20:
    print("x positivo y < 20")

# b) Early return / guard clauses
def procesar_valor(x):
    if x <= 0:
        return "Valor no válido"
    # lógica principal
    return f"Procesando {x}"

print(procesar_valor(-5))
print(procesar_valor(15))

# c) Evitar condiciones redundantes
a = True
b = False

# ❌ Malo
if a == True and b == False:
    print("Condición redundante")

# ✅ Mejor
if a and not b:
    print("Condición clara y legible")

# =========================================================
# 3. Uso profesional en backend
# =========================================================

def validar_usuario(edad, activo):
    if edad < 18:
        return "Usuario menor de edad"
    elif not activo:
        return "Usuario inactivo"
    else:
        return "Usuario válido"

print(validar_usuario(17, True))
print(validar_usuario(25, False))
print(validar_usuario(30, True))

# =========================================================
# 4. Notas clave
# =========================================================

"""
- if / elif / else deben ser legibles y concisos
- Evitar anidamientos innecesarios usando operadores compuestos y guard clauses
- Las condiciones deben ser claras, no sobrecomplicadas
- Backend/data: condicionales claras → endpoints y pipelines robustos y testables
"""
