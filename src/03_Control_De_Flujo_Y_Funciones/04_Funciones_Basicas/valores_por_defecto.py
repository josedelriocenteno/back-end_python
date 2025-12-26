# valores_por_defecto.py
"""
VALORES POR DEFECTO EN PYTHON
==============================

Objetivo:
- Entender cómo funcionan los valores por defecto en parámetros
- Evitar errores comunes y efectos inesperados
- Aplicable a backend, APIs y pipelines de datos
"""

# =========================================================
# 1. Valor por defecto simple
# =========================================================

def saludar(nombre="Invitado"):
    print(f"Hola, {nombre}!")

saludar()           # Hola, Invitado!
saludar("Ana")      # Hola, Ana!

# =========================================================
# 2. Valores por defecto con tipos mutables (cuidado)
# =========================================================

def agregar_item_lista(item, lista=[]):
    lista.append(item)
    return lista

print(agregar_item_lista(1))  # [1]
print(agregar_item_lista(2))  # [1, 2] ❌ Lista compartida

# Solución correcta
def agregar_item_lista_segura(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista

print(agregar_item_lista_segura(1))  # [1]
print(agregar_item_lista_segura(2))  # [2] ✅ Lista separada

# =========================================================
# 3. Mezcla con parámetros posicionales y nombrados
# =========================================================

def crear_usuario(nombre, rol="usuario", activo=True):
    return {"nombre": nombre, "rol": rol, "activo": activo}

usuario1 = crear_usuario("Ana")
usuario2 = crear_usuario("Luis", activo=False)
print(usuario1, usuario2)

# =========================================================
# 4. Buenas prácticas reales
# =========================================================

# - Nunca usar mutable como valor por defecto (list, dict, set)
# - Usa None + inicialización dentro de la función
# - Mantén coherencia: valores por defecto deben ser inmutables o controlados
# - Documenta en docstrings los valores por defecto
# - Facilita la legibilidad usando keyword arguments al llamar la función
