# break_continue_pass.py
"""
break, continue y pass en Backend Python – Uso Profesional

Este módulo explica:
- Qué hace realmente cada palabra clave
- Cuándo usarlas y cuándo NO
- Errores reales en producción
- Patrones claros y mantenibles
"""

# -------------------------------------------------
# 1. break – salir del bucle
# -------------------------------------------------

# ✔️ Uso correcto: terminar cuando ya no hace falta seguir
for usuario in ["ana", "juan", "lucia"]:
    if usuario == "juan":
        print("Usuario encontrado")
        break

# ❌ Error común: break mal colocado
# for u in usuarios:
#     break  # bucle inútil


# -------------------------------------------------
# 2. continue – saltar iteración actual
# -------------------------------------------------

for i in range(5):
    if i % 2 == 0:
        continue  # saltar pares
    print(i)

# ✔️ Útil para filtros simples


# -------------------------------------------------
# 3. pass – NO hacer nada (literalmente)
# -------------------------------------------------

# pass existe para mantener sintaxis válida

def funcion_pendiente():
    pass  # implementación futura


# -------------------------------------------------
# 4. Error típico: usar pass como parche
# -------------------------------------------------

# ❌ Código peligroso
def validar(usuario):
    if not usuario:
        pass  # ❌ no valida nada

# ✔️ Profesional
def validar(usuario):
    if not usuario:
        raise ValueError("Usuario inválido")


# -------------------------------------------------
# 5. break vs return
# -------------------------------------------------

# ❌ Confuso
def buscar_malo(lista, objetivo):
    encontrado = False
    for x in lista:
        if x == objetivo:
            encontrado = True
            break
    return encontrado

# ✔️ Claro
def buscar_bueno(lista, objetivo):
    for x in lista:
        if x == objetivo:
            return True
    return False


# -------------------------------------------------
# 6. continue vs if
# -------------------------------------------------

# ❌ Anidamiento innecesario
for i in range(10):
    if i % 2 != 0:
        print(i)

# ✔️ Guard clause
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)


# -------------------------------------------------
# 7. pass en clases (uso real)
# -------------------------------------------------

class BaseHandler:
    pass


# -------------------------------------------------
# 8. break en while (zona crítica)
# -------------------------------------------------

contador = 0
while True:
    contador += 1
    if contador == 3:
        break  # sin esto, loop infinito


# -------------------------------------------------
# 9. Error común de junior
# -------------------------------------------------
# ❌ pass para silenciar errores
# ❌ break sin lógica clara
# ❌ continue escondiendo bugs
# ❌ flujo difícil de seguir


# -------------------------------------------------
# 10. Checklist mental backend
# -------------------------------------------------
# ✔️ ¿Puedo salir antes?
# ✔️ ¿Estoy ocultando un error?
# ✔️ ¿Esto mejora la legibilidad?
# ✔️ ¿Hay una alternativa más clara?


# -------------------------------------------------
# 11. Regla de oro
# -------------------------------------------------
"""
Si usas pass para evitar pensar,
estás escribiendo bugs.
"""
