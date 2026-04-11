"""
errores_http.py
================

Objetivo:
- Entender la diferencia entre errores 4xx y 5xx
- Aprender a manejar y devolver errores HTTP de forma profesional
- Mantener APIs limpias y consistentes
"""

# -------------------------------------------------------------------
# 1️⃣ ERRORES HTTP: CONCEPTO
# -------------------------------------------------------------------

# HTTP define códigos de estado:
# - 2xx → Éxito
# - 3xx → Redirecciones
# - 4xx → Errores del cliente (mal request)
# - 5xx → Errores del servidor (problemas internos)

# Diferencia clave:
# - 4xx → El cliente envió algo incorrecto
# - 5xx → Fallo del servidor, no culpa del cliente

# -------------------------------------------------------------------
# 2️⃣ EJEMPLOS PRÁCTICOS
# -------------------------------------------------------------------

# Simulando un endpoint de API en Python (sin framework)
def obtener_usuario_api(user_id):
    usuarios = {1: "Alice", 2: "Bob"}

    if not isinstance(user_id, int):
        # ❌ Error del cliente → 400 Bad Request
        return {"error": "user_id debe ser un entero"}, 400

    if user_id not in usuarios:
        # ❌ Error del cliente → 404 Not Found
        return {"error": f"Usuario {user_id} no encontrado"}, 404

    # ✅ Éxito
    return {"user_id": user_id, "nombre": usuarios[user_id]}, 200

# Ejemplo de fallo interno del servidor
def procesar_pedido(pedido):
    try:
        # Simulamos error inesperado
        resultado = 10 / 0
        return {"resultado": resultado}, 200
    except ZeroDivisionError as e:
        # ❌ Error del servidor → 500 Internal Server Error
        return {"error": "Error interno del servidor"}, 500

# -------------------------------------------------------------------
# 3️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Diferenciar claramente 4xx vs 5xx
# 2️⃣ Incluir mensaje útil pero sin exponer detalles sensibles
# 3️⃣ Mantener consistencia en la estructura de respuesta
#    Ejemplo de respuesta JSON uniforme:
#    {
#        "status": 404,
#        "error": "Recurso no encontrado",
#        "timestamp": "2026-01-06T12:00:00Z"
#    }
# 4️⃣ Loggear errores internos (5xx) para depuración sin exponer al cliente
# 5️⃣ Validar entrada de usuario y lanzar 4xx antes de ejecutar lógica crítica
# 6️⃣ Evitar usar 200 OK con mensajes de error → rompe consistencia y clientes

# -------------------------------------------------------------------
# 4️⃣ EJEMPLO DE RESPUESTA PROFESIONAL
# -------------------------------------------------------------------

import datetime
import json

def respuesta_json(mensaje: str, codigo: int):
    return json.dumps({
        "status": codigo,
        "error": mensaje if codigo >= 400 else None,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), codigo

# Uso:
print(respuesta_json("Usuario no encontrado", 404))
print(respuesta_json("Pedido procesado correctamente", 200))
print(respuesta_json("Error interno del servidor", 500))

# -------------------------------------------------------------------
# 5️⃣ RESUMEN
# -------------------------------------------------------------------

# - 4xx → Errores del cliente (mal request, datos faltantes, no autorizado)
# - 5xx → Errores internos del servidor (bugs, excepciones no manejadas)
# - Siempre retornar JSON consistente
# - Loggear 5xx y no exponer stack traces al cliente
# - Validar input para minimizar 4xx y errores inesperados
