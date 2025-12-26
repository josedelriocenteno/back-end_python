# errores_condicionales_comunes.py
"""
ERRORES COMUNES EN CONDICIONALES
================================

Objetivo:
- Identificar y evitar los errores típicos en condicionales: if anidados, condiciones redundantes
- Mejorar legibilidad y mantenimiento del código
- Aplicable a backend, pipelines de datos y sistemas profesionales
"""

# =========================================================
# 1. IF ANIDADOS PROFUNDOS
# =========================================================

x = 10
y = 5
z = 3

# ❌ Código confuso con demasiados niveles
if x > 0:
    if y > 0:
        if z > 0:
            print("Todos positivos")

# ✅ Mejor usando operadores compuestos
if x > 0 and y > 0 and z > 0:
    print("Todos positivos")

# =========================================================
# 2. CONDICIONES REDUNDANTES
# =========================================================

a = True
b = False

# ❌ Redundante: comparación explícita con True/False
if a == True and b == False:
    print("Condición redundante")

# ✅ Limpio y legible
if a and not b:
    print("Condición clara y legible")

# =========================================================
# 3. USO DE GUARD CLAUSES PARA EVITAR ANIDAMIENTO
# =========================================================

def procesar_valor(x):
    # ❌ Anidamiento profundo
    if x > 0:
        if x < 100:
            return f"Valor válido: {x}"
        else:
            return "Valor demasiado grande"
    else:
        return "Valor no válido"

# ✅ Early return / guard clauses
def procesar_valor_limpio(x):
    if x <= 0:
        return "Valor no válido"
    if x >= 100:
        return "Valor demasiado grande"
    return f"Valor válido: {x}"

# =========================================================
# 4. ERRORES TÍPICOS DE JUNIORS
# =========================================================

"""
- Mezclar control de flujo con manipulación de datos dentro del mismo if
- Repetir condiciones similares en varios if/elif
- No usar paréntesis cuando combinamos varios operadores lógicos
- Confundir indentación y flujo lógico
"""

# =========================================================
# 5. BUENAS PRÁCTICAS
# =========================================================

"""
- Limitar anidamientos usando guard clauses y operadores compuestos
- Mantener las condiciones claras, legibles y concisas
- Backend/data: endpoints y funciones deben ser fáciles de leer, testear y mantener
- Comprobar siempre los casos límite y negativos primero
"""
