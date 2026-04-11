"""
print_debugging.py
=================

Objetivo:
- Aprender a usar print de manera inteligente para debugging
- Evitar dependencias de print en producción
- Mantener código limpio mientras se detectan errores rápidamente
"""

# -------------------------------------------------------------------
# 1️⃣ CUÁNDO USAR print PARA DEBUGGING
# -------------------------------------------------------------------

# Útil en scripts simples o pruebas rápidas
# Nunca debe reemplazar logging en producción
# Sirve para inspeccionar variables, flujos y valores intermedios

# Ejemplo básico
x = 10
y = 0

print("DEBUG: valores iniciales", x, y)  # Mensaje temporal para debugging

# -------------------------------------------------------------------
# 2️⃣ PRINT CON CONTEXTO CLARO
# -------------------------------------------------------------------

# Siempre indicar qué se está mostrando
lista = [1, 2, 3]
print("DEBUG: contenido de la lista:", lista)

# Evitar prints ambiguos como:
# print(lista)  # ❌ Mala práctica

# -------------------------------------------------------------------
# 3️⃣ USAR F-STRINGS PARA CLARIDAD
# -------------------------------------------------------------------

nombre = "Juan"
edad = 18
print(f"DEBUG: Usuario={nombre}, Edad={edad}")

# Más legible y fácil de buscar en consola

# -------------------------------------------------------------------
# 4️⃣ EVITAR PRINTS EN BUCLES MASIVOS
# -------------------------------------------------------------------

# ❌ Mala práctica
for i in range(1000):
    print(i)  # saturará la consola y será difícil de depurar

# ✅ Alternativa: imprimir solo puntos de control
for i in range(1000):
    if i % 100 == 0:
        print(f"DEBUG: avance {i}/1000")

# -------------------------------------------------------------------
# 5️⃣ TEMPORALIDAD DE PRINTS
# -------------------------------------------------------------------

# Print solo durante desarrollo
# Siempre eliminar o reemplazar por logging antes de entregar código

# Ejemplo:
debug_mode = True
if debug_mode:
    print(f"DEBUG: variables x={x}, y={y}")

# -------------------------------------------------------------------
# 6️⃣ RESUMEN DE USO INTELIGENTE
# -------------------------------------------------------------------

# 1. Print solo para debugging temporal
# 2. Siempre agregar contexto: qué variable o flujo se está mostrando
# 3. Usar f-strings para claridad
# 4. No saturar la consola con loops masivos
# 5. Reemplazar por logging antes de pasar a producción
# 6. Evitar print de información sensible

# -------------------------------------------------------------------
# 7️⃣ EJEMPLO COMPLETO
# -------------------------------------------------------------------

def calcular_promedio(lista):
    if not lista:
        print("DEBUG: lista vacía")  # temporal
        return 0
    total = sum(lista)
    promedio = total / len(lista)
    print(f"DEBUG: total={total}, longitud={len(lista)}, promedio={promedio}")
    return promedio

calcular_promedio([10, 20, 30])
calcular_promedio([])
