# operadores_logicos.py
"""
OPERADORES LÓGICOS EN PYTHON
============================

Objetivo:
- Comprender and, or, not y su comportamiento de cortocircuito
- Escribir condicionales legibles y eficientes
- Preparar código profesional para backend y pipelines
"""

# =========================================================
# 1. AND, OR, NOT básicos
# =========================================================

a = True
b = False

print(f"a and b: {a and b}")  # False
print(f"a or b: {a or b}")    # True
print(f"not a: {not a}")      # False

# =========================================================
# 2. Cortocircuito (Short-circuit)
# =========================================================

def funcion_lenta():
    print("Ejecutando función lenta...")
    return True

# AND cortocircuita si el primer valor es False
print("AND cortocircuito")
resultado = False and funcion_lenta()  # funcion_lenta NO se ejecuta
print(f"Resultado: {resultado}")

# OR cortocircuita si el primer valor es True
print("OR cortocircuito")
resultado = True or funcion_lenta()    # funcion_lenta NO se ejecuta
print(f"Resultado: {resultado}")

# =========================================================
# 3. Uso profesional en condicionales
# =========================================================

edad = 25
activo = True
premium = False

# Evitar anidamientos innecesarios
if edad >= 18 and activo:
    print("Usuario activo y mayor de edad")

# OR para condiciones alternativas
if premium or edad < 18:
    print("Usuario premium o menor de edad")

# NOT para negación
if not premium:
    print("Usuario NO premium")

# =========================================================
# 4. Trucos y buenas prácticas
# =========================================================

# - Combinar operadores de forma legible: evita cosas como "not a and b or c"
# - Usa paréntesis para claridad si hay múltiples operadores
# - Aprovecha cortocircuito para evitar cálculos innecesarios

# Ejemplo: safe division
numerador = 10
denominador = 0

if denominador != 0 and numerador / denominador > 1:
    print("Division > 1")
else:
    print("No se puede dividir o <= 1")

# =========================================================
# 5. Resumen profesional
# =========================================================

"""
- and: True si ambos operandos son True, cortocircuita en False
- or: True si al menos uno es True, cortocircuita en True
- not: invierte booleano
- Cortocircuito: mejora eficiencia y previene errores (como division por cero)
- Backend/data: condicionales limpias y eficientes → endpoints y pipelines robustos
"""
