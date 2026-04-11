"""
errores_vs_validaciones.py
==========================

Objetivo:
- Diferenciar entre validaciones y errores
- Saber cuándo lanzar excepciones y cuándo manejar inputs silenciosamente
- Mejorar robustez y claridad del código
"""

# -------------------------------------------------------------------
# 1️⃣ CUÁNDO VALIDAR
# -------------------------------------------------------------------

# Validar significa comprobar que los datos cumplen ciertos criterios
# Antes de ejecutar la lógica principal, sin necesariamente lanzar errores.

def procesar_usuario(usuario: dict):
    # Validación básica
    if "nombre" not in usuario:
        # Podemos dar valor por defecto o loguear warning
        usuario["nombre"] = "Anonimo"
        print("Advertencia: nombre faltante, usando 'Anonimo'")
    if "email" not in usuario or "@" not in usuario["email"]:
        # Valor por defecto o corrección automática
        usuario["email"] = "default@example.com"
        print("Advertencia: email inválido, usando valor por defecto")
    return usuario

# Uso
usuario = {"edad": 25}
usuario_corregido = procesar_usuario(usuario)
print(usuario_corregido)
# Output:
# Advertencia: nombre faltante, usando 'Anonimo'
# Advertencia: email inválido, usando valor por defecto
# {'edad': 25, 'nombre': 'Anonimo', 'email': 'default@example.com'}

# -------------------------------------------------------------------
# 2️⃣ CUÁNDO LANZAR ERRORES
# -------------------------------------------------------------------

# Lanzar excepciones cuando los datos son críticos y no se puede continuar
def crear_producto(nombre: str, precio: float):
    if not nombre:
        raise ValueError("Nombre obligatorio")
    if precio < 0:
        raise ValueError("Precio no puede ser negativo")
    return {"nombre": nombre, "precio": precio}

# Uso
try:
    crear_producto("", -50)
except ValueError as e:
    print(f"Error crítico: {e}")
# Output: Error crítico: Nombre obligatorio

# -------------------------------------------------------------------
# 3️⃣ PRINCIPIOS PARA DECIDIR
# -------------------------------------------------------------------

# 1️⃣ Validar inputs opcionales o recuperables:
#     - Dar valores por defecto
#     - Loguear advertencia
#     - No interrumpir ejecución
# 2️⃣ Lanzar errores para inputs obligatorios o críticos:
#     - Datos que rompen la lógica
#     - Estado que puede corromper resultados
# 3️⃣ Usar fail-fast: detectar errores antes de ejecutar lógica compleja
# 4️⃣ Evitar capturar excepciones genéricas solo para continuar el flujo

# -------------------------------------------------------------------
# 4️⃣ EJEMPLO COMPLETO
# -------------------------------------------------------------------

def procesar_pedido(pedido: dict):
    # Validaciones suaves
    if "descuento" not in pedido:
        pedido["descuento"] = 0
        print("Advertencia: sin descuento, usando 0")
    # Validaciones críticas
    if "productos" not in pedido or len(pedido["productos"]) == 0:
        raise ValueError("Pedido debe contener al menos un producto")
    return pedido

# Uso
pedido = {"cliente": "Juan"}
try:
    procesar_pedido(pedido)
except ValueError as e:
    print(f"Error crítico: {e}")
# Output:
# Advertencia: sin descuento, usando 0
# Error crítico: Pedido debe contener al menos un producto

# -------------------------------------------------------------------
# 5️⃣ RESUMEN
# -------------------------------------------------------------------

# - Validaciones suaves: inputs opcionales, recuperables, loguear advertencias
# - Errores críticos: inputs obligatorios, lógica central, fallar rápido
# - Mantener consistencia y claridad en la estrategia
# - Combinación de validaciones y fail-fast = robustez máxima
