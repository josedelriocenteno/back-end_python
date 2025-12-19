# patrones_condicionales.py
"""
PATRONES DE CONDICIONALES
=========================

Objetivo:
- Aprender a usar guard clauses y early return para condicionales claras y profesionales
- Evitar anidamientos profundos y código spaghetti
- Preparar código limpio y mantenible en backend y pipelines de datos
"""

# =========================================================
# 1. Problema típico: condicionales anidadas
# =========================================================

def procesar_valor_malo(x):
    if x > 0:
        if x < 100:
            print(f"Valor válido: {x}")
        else:
            print("Valor demasiado grande")
    else:
        print("Valor no válido")

# ❌ Código difícil de leer y mantener

# =========================================================
# 2. Guard Clauses / Early Return
# =========================================================

def procesar_valor_bueno(x):
    if x <= 0:
        return "Valor no válido"
    if x >= 100:
        return "Valor demasiado grande"
    # flujo principal
    return f"Valor válido: {x}"

print(procesar_valor_bueno(-5))   # Valor no válido
print(procesar_valor_bueno(150))  # Valor demasiado grande
print(procesar_valor_bueno(50))   # Valor válido: 50

# =========================================================
# 3. Ventajas
# =========================================================

"""
- Reduce la indentación y mejora la legibilidad
- Facilita testing de casos extremos
- El flujo principal del método queda limpio y fácil de seguir
- Muy útil en endpoints de backend y funciones de pipelines de datos
"""

# =========================================================
# 4. Aplicación profesional
# =========================================================

def validar_usuario(edad, activo):
    if edad < 18:
        return "Usuario menor de edad"
    if not activo:
        return "Usuario inactivo"
    # flujo principal
    return "Usuario válido"

print(validar_usuario(17, True))   # Usuario menor de edad
print(validar_usuario(25, False))  # Usuario inactivo
print(validar_usuario(30, True))   # Usuario válido

# =========================================================
# 5. Buenas prácticas
# =========================================================

"""
- Siempre manejar primero casos de error o excepciones (guard clauses)
- Dejar el flujo principal "limpio", sin anidamientos innecesarios
- Combinar con operadores lógicos claros para legibilidad
- Backend/data: endpoints claros, validaciones rápidas y testables
"""
