"""
codigo_que_funciona_vs_codigo_mantenible.py
===========================================

Este archivo demuestra, CON CÓDIGO REAL, la diferencia entre:

1) Código que simplemente funciona
2) Código mantenible, extensible y profesional

No se trata de patrones por postureo.
Se trata de escribir código que sobreviva al cambio.

Lee los comentarios con calma. Están puestos a propósito.
"""

# -------------------------------------------------------------------
# EJEMPLO 1: CÓDIGO QUE FUNCIONA (PERO NO ESCALA)
# -------------------------------------------------------------------

def calcular_total_codigo_sucio(pedidos, tipo_usuario):
    """
    Calcula el total de una lista de pedidos aplicando un descuento
    según el tipo de usuario.

    Este código FUNCIONA.
    El problema es que es frágil y difícil de mantener.
    """

    total = 0

    # Sumamos precios (asumimos que pedidos es una lista de diccionarios)
    for pedido in pedidos:
        total += pedido["precio"]

    # Lógica de negocio mezclada con cálculo
    if tipo_usuario == "normal":
        total = total
    elif tipo_usuario == "promo":
        total = total * 0.9
    elif tipo_usuario == "premium":
        total = total * 0.85

    return total


# -----------------------------
# PROBLEMAS DE ESTE ENFOQUE:
# -----------------------------
#
# 1. La función hace demasiadas cosas:
#    - recorre pedidos
#    - suma precios
#    - decide descuentos
#    - aplica reglas de negocio
#
# 2. Si aparece un nuevo tipo de usuario, hay que modificar esta función.
#
# 3. Usa diccionarios sin garantías (pedido["precio"]).
#
# 4. Es difícil de testear por partes.
#
# En proyectos reales, este tipo de código envejece MUY mal.


# -------------------------------------------------------------------
# EJEMPLO 2: CÓDIGO MANTENIBLE (MISMA FUNCIONALIDAD, MEJOR DISEÑO)
# -------------------------------------------------------------------

# Primero, modelamos mejor los datos.
# Usamos una clase simple en lugar de diccionarios sueltos.

class Pedido:
    """
    Representa un pedido individual.

    Esta clase SOLO representa datos.
    No aplica descuentos ni reglas complejas.
    """

    def __init__(self, precio: float):
        self.precio = precio


# ------------------------------------------------
# PASO 1: UNA FUNCIÓN = UNA RESPONSABILIDAD
# ------------------------------------------------

def calcular_subtotal(pedidos: list[Pedido]) -> float:
    """
    Calcula el subtotal de una lista de pedidos.

    - No sabe nada de descuentos
    - No sabe nada del tipo de usuario
    - Solo suma precios

    Esto hace que sea:
    - fácil de entender
    - fácil de testear
    """

    return sum(pedido.precio for pedido in pedidos)


# ------------------------------------------------
# PASO 2: DESCUENTOS COMO COMPORTAMIENTOS AISLADOS
# ------------------------------------------------

class DescuentoNormal:
    """No aplica descuento."""

    def aplicar(self, subtotal: float) -> float:
        return subtotal


class DescuentoPromo:
    """Aplica un 10% de descuento."""

    def aplicar(self, subtotal: float) -> float:
        return subtotal * 0.9


class DescuentoPremium:
    """Aplica un 15% de descuento."""

    def aplicar(self, subtotal: float) -> float:
        return subtotal * 0.85


# ------------------------------------------------
# PASO 3: COMPOSICIÓN EN LUGAR DE CONDICIONALES
# ------------------------------------------------

def calcular_total_codigo_limpio(
    pedidos: list[Pedido],
    estrategia_descuento
) -> float:
    """
    Calcula el total usando una estrategia de descuento.

    Observa algo importante:
    - No hay ifs
    - No hay conocimiento del tipo de usuario
    - El comportamiento se inyecta desde fuera

    Este diseño resiste el cambio.
    """

    subtotal = calcular_subtotal(pedidos)
    return estrategia_descuento.aplicar(subtotal)


# -------------------------------------------------------------------
# EJECUCIÓN DE EJEMPLO (para ver la diferencia en acción)
# -------------------------------------------------------------------

if __name__ == "__main__":
    pedidos = [
        Pedido(100),
        Pedido(50),
        Pedido(25),
    ]

    total_sucio = calcular_total_codigo_sucio(
        pedidos=[{"precio": 100}, {"precio": 50}, {"precio": 25}],
        tipo_usuario="promo",
    )

    total_limpio = calcular_total_codigo_limpio(
        pedidos=pedidos,
        estrategia_descuento=DescuentoPromo(),
    )

    print("Total código sucio:", total_sucio)
    print("Total código limpio:", total_limpio)


# -------------------------------------------------------------------
# CONCLUSIÓN (IMPORTANTE)
# -------------------------------------------------------------------
#
# Ambos enfoques dan el MISMO resultado.
#
# La diferencia es que:
# - el primero se rompe cuando el sistema crece
# - el segundo se adapta al cambio sin dolor
#
# En backend, data e IA:
# - el cambio es constante
# - la mantenibilidad NO es opcional
#
# Este archivo no busca ser elegante.
# Busca ser sostenible.
