# funciones_idempotentes.py
"""
FUNCIONES IDEMPOTENTES
=====================

Objetivo:
- Comprender y aplicar idempotencia en funciones y endpoints
- Evitar efectos secundarios no deseados en sistemas distribuidos
- Facilitar reintentos seguros, consistencia y testabilidad
"""

from typing import Dict, Any

# =========================================================
# 1. Qué significa idempotencia
# =========================================================
# Una función es idempotente si múltiples llamadas con los mismos parámetros
# producen el mismo efecto y resultado, sin causar errores ni duplicaciones.

# Ejemplo conceptual:
estado_global = {}

def ejemplo_no_idempotente(usuario_id: int):
    """No idempotente: incrementa contador cada vez que se llama"""
    if usuario_id not in estado_global:
        estado_global[usuario_id] = 0
    estado_global[usuario_id] += 1
    return estado_global[usuario_id]

# =========================================================
# 2. Función idempotente
# =========================================================
def ejemplo_idempotente(usuario_id: int, valor: int) -> Dict[str, Any]:
    """
    Función idempotente: múltiples llamadas con los mismos argumentos
    producen el mismo resultado y estado.

    Args:
        usuario_id (int): ID del usuario
        valor (int): Valor a asignar

    Returns:
        dict: Estado actualizado
    """
    # En sistemas reales, se aplicaría un upsert en base de datos
    estado_global[usuario_id] = valor  # Sobrescribe, no incrementa
    return {"usuario_id": usuario_id, "valor": estado_global[usuario_id]}

# =========================================================
# 3. Uso en APIs
# =========================================================
def actualizar_config_endpoint(usuario_id: int, config: dict) -> Dict[str, Any]:
    """
    Endpoint idempotente: reintentos seguros sin duplicar efectos.
    """
    # Simulación: se reemplaza completamente la configuración
    estado_global[usuario_id] = config.copy()  # Copia para evitar referencias externas
    return {"mensaje": "Configuración aplicada correctamente", "config": estado_global[usuario_id]}

# =========================================================
# 4. Buenas prácticas profesionales
# =========================================================
# - Diseñar funciones de mutación de estado de manera que sean idempotentes
# - En APIs: PUT suele ser idempotente, POST no necesariamente
# - Evitar efectos secundarios no controlados (prints, logs mutables)
# - Documentar claramente que la función es idempotente
# - Test unitario: llamar varias veces con los mismos datos y verificar consistencia
# - Útil en pipelines distribuidos: reintentos seguros, tolerancia a fallos
