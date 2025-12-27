# ❌ MAL - Lista de sesiones activas
sesiones_activas = []  # 10k elementos

def obtener_sesion(session_id):
    for sesion in sesiones_activas:  # O(10k) = 100ms por request!
        if sesion['id'] == session_id:
            return sesion
    return None

# PROBLEMA: 100ms x 1000 req/s = 100s CPU desperdiciado
# SOLUCIÓN: dict {session_id: datos} → O(1)

# ❌ MAL - Cola con listas
cola_tareas = []

def procesar_siguiente():
    return cola_tareas.pop(0)  # O(n) mueve 1M tareas!

# Con 1M tareas pendientes:
# pop(0) = 1M operaciones → 5+ SEGUNDOS por tarea 😱
