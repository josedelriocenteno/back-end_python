"""
funciones_pequenas.py
=====================

Este archivo enseña la regla de oro de funciones limpias:
**Una función = una sola responsabilidad / una sola cosa**.

Beneficios:
- Facilita pruebas unitarias
- Mejora legibilidad
- Reduce bugs y dependencias ocultas
- Permite reutilización y refactor seguro
"""

# -------------------------------------------------------------------
# 1️⃣ PROBLEMA CLÁSICO: FUNCIONES GIGANTES
# -------------------------------------------------------------------

# ❌ MAL: hace demasiadas cosas
def procesar_datos_gigante(datos: list[int]) -> float:
    """
    1. Filtra valores negativos
    2. Calcula suma total
    3. Imprime resultado
    4. Devuelve promedio
    """
    positivos = [x for x in datos if x >= 0]
    total = sum(positivos)
    print(f"Total: {total}")
    promedio = total / len(positivos)
    return promedio

# Problema:
# - Mezcla lógica, I/O y cálculo
# - Difícil de testear
# - Si cambia un paso, afecta todo lo demás


# -------------------------------------------------------------------
# 2️⃣ SOLUCIÓN: FUNCIONES PEQUEÑAS Y CLARAS
# -------------------------------------------------------------------

def filtrar_positivos(datos: list[int]) -> list[int]:
    """Devuelve solo los números >= 0."""
    return [x for x in datos if x >= 0]

def calcular_total(datos: list[int]) -> int:
    """Suma todos los valores de la lista."""
    return sum(datos)

def calcular_promedio(datos: list[int]) -> float:
    """Calcula la media aritmética."""
    if not datos:
        return 0.0
    return sum(datos) / len(datos)

def imprimir_total(total: int) -> None:
    """Imprime el total en formato legible."""
    print(f"Total: {total}")


# -------------------------------------------------------------------
# 3️⃣ FUNCIÓN PRINCIPAL COMO ORQUESTADOR
# -------------------------------------------------------------------

def procesar_datos(datos: list[int]) -> float:
    """
    Orquesta la ejecución usando funciones pequeñas.

    Retorna:
        float: promedio de los valores positivos.
    """
    positivos = filtrar_positivos(datos)
    total = calcular_total(positivos)
    imprimir_total(total)
    return calcular_promedio(positivos)


# -------------------------------------------------------------------
# 4️⃣ VENTAJAS DE ESTE ENFOQUE
# -------------------------------------------------------------------
#
# - Cada función hace **una sola cosa**
# - Fácil de testear por separado
# - Fácil de refactorizar sin romper todo
# - Facilita debugging y comprensión rápida
# - Reutilizable en otros contextos


# -------------------------------------------------------------------
# 5️⃣ REGLA DE ORO
# -------------------------------------------------------------------
#
# Una función debe:
# 1. Tener un único propósito
# 2. Tener un nombre claro que explique qué hace
# 3. Tener pocos parámetros (ideal: < 3)
# 4. Evitar efectos secundarios ocultos
# 5. No mezclar cálculos, I/O, lógica de negocio o transformaciones


# -------------------------------------------------------------------
# 6️⃣ EJEMPLO PRÁCTICO PARA PROYECTO POO
# -------------------------------------------------------------------

# Supongamos tu PedidoService:

def calcular_total_pedido(productos: list["Producto"]) -> float:
    """Calcula total de un pedido."""
    return sum(p.precio for p in productos)

def aplicar_descuento(total: float, descuento: float) -> float:
    """Aplica descuento al total y devuelve el final."""
    return total * (1 - descuento)

def mostrar_resumen_pedido(total: float) -> None:
    """Imprime resumen del pedido."""
    print(f"Total final del pedido: ${total:.2f}")


def procesar_pedido(productos: list["Producto"], descuento: float) -> float:
    """Orquesta cálculo de pedido aplicando descuento y mostrando resumen."""
    total = calcular_total_pedido(productos)
    total_final = aplicar_descuento(total, descuento)
    mostrar_resumen_pedido(total_final)
    return total_final


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Funciones pequeñas = código mantenible y profesional
# Siempre pregunta: "¿Esta función hace solo una cosa?"
# Si la respuesta es no, divídela en partes más pequeñas
