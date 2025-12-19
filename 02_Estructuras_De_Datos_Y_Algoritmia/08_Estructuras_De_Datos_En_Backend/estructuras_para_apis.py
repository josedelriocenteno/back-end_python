# estructuras_para_apis.py
"""
ESTRUCTURAS DE DATOS PARA ENDPOINTS — BACKEND PROFESIONAL
=========================================================

Objetivo:
- Elegir la estructura adecuada según tipo de datos y operación
- Mejorar performance de APIs y microservicios
- Evitar errores comunes de juniors en endpoints
"""

# ------------------------------------------------------------
# 1. LISTAS PARA ORDEN Y SECUENCIAS
# ------------------------------------------------------------

# Útil para:
# - Retornar colecciones ordenadas
# - Almacenar elementos donde el orden importa
# - Iteraciones y paginaciones

usuarios = ["alice", "bob", "carol"]
# Retornar todos los usuarios
def get_usuarios():
    return usuarios  # O(n) iteración, O(1) append al final

# Precaución: listas grandes → O(n) en búsquedas
print("Usuarios:", get_usuarios())


# ------------------------------------------------------------
# 2. DICCIONARIOS PARA BÚSQUEDA RÁPIDA
# ------------------------------------------------------------

# Útil para:
# - Acceso por clave rápida → O(1) promedio
# - JSON response típico
# - Lookup tables en endpoints

usuario_info = {
    "alice": {"edad": 30, "rol": "admin"},
    "bob": {"edad": 25, "rol": "user"}
}

def get_usuario(nombre):
    return usuario_info.get(nombre, None)  # O(1)
    
print("Info de alice:", get_usuario("alice"))


# ------------------------------------------------------------
# 3. SETS PARA MEMBERSHIP TEST
# ------------------------------------------------------------

# Útil para:
# - Verificar existencia rápidamente → O(1)
# - Evitar duplicados
# - Validación de permisos, roles o IDs

ids_permitidos = {101, 102, 103}

def check_id(id):
    return id in ids_permitidos

print("ID 102 permitido:", check_id(102))


# ------------------------------------------------------------
# 4. COMBINACIÓN DE ESTRUCTURAS
# ------------------------------------------------------------

# Ejemplo real: endpoint que retorna solo usuarios activos con info
usuarios_activos = ["alice", "bob", "carol"]
usuarios_activos_set = set(usuarios_activos)

def get_info_usuarios_activos(info_dict, activos_set):
    # Filtrar diccionario usando set → O(1) membership
    return {k: v for k, v in info_dict.items() if k in activos_set}

print("Usuarios activos info:", get_info_usuarios_activos(usuario_info, usuarios_activos_set))


# ------------------------------------------------------------
# 5. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usa listas para secuencias y orden
✔ Usa diccionarios para lookups rápidos y JSON responses
✔ Usa sets para membership test y eliminar duplicados
✔ Evita loops innecesarios → aprovecha estructuras eficientes
✔ Documenta el tipo de retorno de endpoints (list, dict, set)
✔ Piensa en performance O(1)/O(n) antes de exponer el endpoint
✔ Mantén endpoints claros y consistentes
"""

print("Estructuras de datos para endpoints dominadas profesionalmente")
