# argumentos_posicionales_y_nominales.py
"""
Argumentos Posicionales y Nominales en Funciones Python – Nivel Profesional

Este módulo cubre:
- Diferencia entre args posicionales y kwargs nombrados
- Cuándo usar cada uno
- Errores típicos en backend
- Patrones claros y mantenibles
"""

# -------------------------------------------------
# 1. Argumentos posicionales
# -------------------------------------------------

def sumar(a: int, b: int) -> int:
    """
    Suma dos números.
    """
    return a + b

# Llamada posicional: el orden importa
resultado = sumar(3, 5)
print(resultado)  # 8

# ❌ Error común: confundir orden
# resultado = sumar(5, 3)  # puede no ser lo que querías


# -------------------------------------------------
# 2. Argumentos nombrados (keyword arguments)
# -------------------------------------------------

def crear_usuario(nombre: str, edad: int, rol: str = "user"):
    return {"nombre": nombre, "edad": edad, "rol": rol}

# Llamada nominal: más clara, no depende del orden
usuario = crear_usuario(edad=25, nombre="Ana")
print(usuario)


# -------------------------------------------------
# 3. Mezcla de posicional y nominal
# -------------------------------------------------

# ✔️ Posicional primero, luego nombrado
usuario = crear_usuario("Juan", edad=30, rol="admin")

# ❌ No puedes poner nombre antes del posicional
# usuario = crear_usuario(nombre="Juan", 30, rol="admin")  # SyntaxError


# -------------------------------------------------
# 4. Valores por defecto y nominal
# -------------------------------------------------

# Permite saltarse parámetros opcionales
usuario = crear_usuario("Lucia", edad=22)  # rol por defecto "user"


# -------------------------------------------------
# 5. *args y **kwargs – argumentos variables
# -------------------------------------------------

# Posicional variable
def sumar_todos(*numeros: int) -> int:
    return sum(numeros)

print(sumar_todos(1, 2, 3, 4))  # 10

# Nominal variable
def crear_usuario_completo(nombre, **info):
    usuario = {"nombre": nombre}
    usuario.update(info)
    return usuario

usuario = crear_usuario_completo("Ana", rol="admin", activo=True)
print(usuario)


# -------------------------------------------------
# 6. Errores comunes de juniors
# -------------------------------------------------
# ❌ Mezclar demasiado posicional y nombrado
# ❌ Cambiar orden sin pensar
# ❌ Pasar kwargs sin validar → datos inconsistentes
# ❌ No usar default para parámetros opcionales


# -------------------------------------------------
# 7. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Siempre tipar parámetros y retorno
# ✔️ Mantener posicional solo lo obligatorio
# ✔️ Usar nombrado para opcionales o datos sensibles
# ✔️ Evitar confusión en llamadas
# ✔️ Revisar *args y **kwargs solo si es necesario


# -------------------------------------------------
# 8. Checklist mental backend
# -------------------------------------------------
# ✔️ Orden claro y lógico?
# ✔️ Nombres de parámetros explícitos?
# ✔️ Defaults seguros?
# ✔️ Evitar errores silenciosos?
# ✔️ Testable y mantenible?


# -------------------------------------------------
# 9. Regla de oro
# -------------------------------------------------
"""
Argumentos posicionales para lo obligatorio, nombrados para claridad y seguridad.
Mejor prevenir confusiones que depurar bugs.
"""
