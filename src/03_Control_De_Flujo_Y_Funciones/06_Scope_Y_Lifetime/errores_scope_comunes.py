# errores_scope_comunes.py
"""
ERRORES COMUNES DE SCOPE EN PYTHON
==================================

Objetivo:
- Identificar y entender los errores silenciosos más frecuentes relacionados con scope y lifetime
- Evitar bugs difíciles de detectar en backend, APIs y pipelines de datos
- Enseñar buenas prácticas para un código limpio y mantenible

Tipos de errores frecuentes:
- Modificar variables globales sin intención
- Confundir variables locales y nonlocal
- Uso incorrecto de closures y lambdas
- Dependencia implícita de variables de scope externo
"""

# =========================================================
# 1. Confusión entre local y global
# =========================================================

contador = 0  # variable global

def incrementar():
    # contador += 1  # ❌ UnboundLocalError: variable local referenciada antes de asignar
    global contador  # ✅ Indicar que queremos usar la global
    contador += 1

incrementar()
print("contador global:", contador)

# Explicación:
# - Python asume que cualquier asignación dentro de una función es local
# - Si quieres modificar la global, usar `global` explícitamente
# - Buen práctica: minimizar uso de globales

# =========================================================
# 2. Confusión con nonlocal
# =========================================================

def factory_contador():
    n = 0  # variable de enclosing

    def incrementar():
        # n += 1  # ❌ UnboundLocalError
        nonlocal n  # ✅ Referencia al scope externo
        n += 1
        return n

    return incrementar

c = factory_contador()
print(c())  # 1
print(c())  # 2

# =========================================================
# 3. Dependencia implícita de scope externo
# =========================================================

valor = 10

def usar_valor():
    # Depende de la existencia de `valor` en scope externo
    return valor * 2

print(usar_valor())  # Funciona, pero es frágil

# Mejor práctica: pasar parámetros explícitos
def usar_valor_seguro(v):
    return v * 2

print(usar_valor_seguro(10))

# =========================================================
# 4. Closures y errores comunes
# =========================================================

funcs = []
for i in range(3):
    funcs.append(lambda: i)  # ❌ Todas las lambdas referencian la misma variable 'i'

print([f() for f in funcs])  # [2, 2, 2]

# ✅ Solución: capturar variable en default argument
funcs_correcto = []
for i in range(3):
    funcs_correcto.append(lambda i=i: i)

print([f() for f in funcs_correcto])  # [0, 1, 2]

# =========================================================
# 5. Buenas prácticas en backend y pipelines
# =========================================================

# - Evitar dependencias implícitas en scope externo
# - Declarar variables lo más local posible
# - Usar parámetros y retornos para pasar datos entre funciones
# - Documentar closures y lambdas para no confundir su contexto
# - Revisar recursión y loops anidados para no saturar stack frames
# - En pipelines de datos, liberar referencias a grandes objetos cuando ya no se usan
