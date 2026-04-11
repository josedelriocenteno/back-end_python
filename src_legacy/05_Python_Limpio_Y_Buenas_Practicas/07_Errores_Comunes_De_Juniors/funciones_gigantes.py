"""
funciones_gigantes.py
=====================

Anti-patrón clásico: Funciones gigantes

Objetivos:
- Identificar funciones demasiado largas
- Mostrar problemas de legibilidad, testabilidad y mantenimiento
- Enseñar estrategias de refactorización paso a paso
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO DE FUNCIÓN GIGANTE
# -------------------------------------------------------------------

# ❌ MAL: esta función hace demasiadas cosas
def procesar_pedido_completo(pedido: dict) -> float:
    """
    1. Valida usuario
    2. Valida productos
    3. Calcula total
    4. Aplica descuentos
    5. Guarda en base de datos
    6. Imprime resumen
    """
    # Validar usuario
    usuario = pedido.get("usuario")
    if not usuario or not usuario.get("activo"):
        print("Usuario inválido")
        return 0.0

    # Validar productos
    productos = pedido.get("productos", [])
    productos_validos = []
    for p in productos:
        if p.get("disponible") and p.get("precio", 0) > 0:
            productos_validos.append(p)
    
    # Calcular total
    total = sum(p["precio"] for p in productos_validos)

    # Aplicar descuento
    tipo_usuario = usuario.get("tipo", "normal")
    if tipo_usuario == "premium":
        total *= 0.85
    elif tipo_usuario == "promo":
        total *= 0.9

    # Guardar en DB (simulado)
    print(f"Guardando pedido para {usuario['nombre']} con total {total}")

    # Imprimir resumen
    print(f"Pedido procesado: Total ${total:.2f}, Usuario: {usuario['nombre']}")
    
    return total


# Problemas de funciones gigantes:
# 1. Difíciles de leer y entender
# 2. Difíciles de testear
# 3. Mezcla múltiples responsabilidades (viola SRP)
# 4. Difíciles de mantener y extender
# 5. Riesgo de errores al cambiar un bloque interno


# -------------------------------------------------------------------
# 2️⃣ REFACTOR PASO 1: EXTRAER FUNCIONES PEQUEÑAS
# -------------------------------------------------------------------

def validar_usuario(usuario: dict) -> bool:
    """Valida si el usuario está activo."""
    return usuario is not None and usuario.get("activo", False)

def filtrar_productos_validos(productos: list[dict]) -> list[dict]:
    """Devuelve solo productos disponibles y con precio > 0."""
    return [p for p in productos if p.get("disponible") and p.get("precio", 0) > 0]

def calcular_total(productos: list[dict]) -> float:
    """Suma los precios de los productos válidos."""
    return sum(p["precio"] for p in productos)

def aplicar_descuento(total: float, tipo_usuario: str) -> float:
    """Aplica descuento según tipo de usuario."""
    if tipo_usuario == "premium":
        return total * 0.85
    elif tipo_usuario == "promo":
        return total * 0.9
    return total

def guardar_pedido(usuario: dict, total: float):
    """Simula persistencia en base de datos."""
    print(f"Guardando pedido para {usuario['nombre']} con total {total}")

def imprimir_resumen(usuario: dict, total: float):
    """Imprime resumen del pedido."""
    print(f"Pedido procesado: Total ${total:.2f}, Usuario: {usuario['nombre']}")


# -------------------------------------------------------------------
# 3️⃣ REFACTOR PASO 2: FUNCIÓN PRINCIPAL LIMPIA
# -------------------------------------------------------------------

def procesar_pedido_limpio(pedido: dict) -> float:
    """Orquesta todas las funciones pequeñas, limpio y legible."""
    usuario = pedido.get("usuario")
    productos = pedido.get("productos", [])

    if not validar_usuario(usuario):
        print("Usuario inválido")
        return 0.0

    productos_validos = filtrar_productos_validos(productos)
    total = calcular_total(productos_validos)
    total = aplicar_descuento(total, usuario.get("tipo", "normal"))
    guardar_pedido(usuario, total)
    imprimir_resumen(usuario, total)
    
    return total


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS DE ESTA REFACTORIZACIÓN
# -------------------------------------------------------------------

# 1. Código mucho más legible
# 2. Funciones pequeñas = fácil de testear individualmente
# 3. SRP aplicado: cada función hace una sola cosa
# 4. Fácil de extender (nuevos tipos de descuento, nueva persistencia)
# 5. Menor riesgo de errores al cambiar la lógica


# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Las funciones gigantes son un anti-patrón clásico de juniors
# Refactorizar a funciones pequeñas:
# - Reduce complejidad
# - Mejora testabilidad
# - Aplica SRP
# - Hace tu código profesional y escalable
