# collections_chainmap.py
"""
COLLECTIONS.CHAINMAP EN PYTHON — COMPOSICIÓN DE DICCIONARIOS
=============================================================

Objetivo:
- Usar ChainMap para combinar múltiples diccionarios
- Buscar claves en varios dicts sin fusionarlos manualmente
- Aplicaciones en backend, configuración y pipelines
"""

from collections import ChainMap

# ------------------------------------------------------------
# 1. CREACIÓN DE UN CHAINMAP
# ------------------------------------------------------------

config_default = {"host": "localhost", "port": 8080}
config_env = {"port": 9090}   # sobreescribe puerto
config_user = {"debug": True}

# Combinar diccionarios en un solo "mapa"
config = ChainMap(config_user, config_env, config_default)
print("ChainMap combinado:", config)

# Acceso a valores
print("Host:", config["host"])      # desde default
print("Port:", config["port"])      # desde env (sobrescribe default)
print("Debug:", config["debug"])    # desde user


# ------------------------------------------------------------
# 2. OPERACIONES BÁSICAS
# ------------------------------------------------------------

# Añadir/modificar valores → afecta al primer dict
config["port"] = 7070
print("Port modificado (afecta al primer dict):", config["port"])
print("Diccionario original del primer nivel:", config.maps[0])

# Agregar nueva clave
config["log_level"] = "INFO"
print("Nueva clave agregada al primer dict:", config.maps[0])

# Recorrer todos los elementos
for key, value in config.items():
    print(f"{key}: {value}")


# ------------------------------------------------------------
# 3. USOS COMUNES
# ------------------------------------------------------------

"""
- Configuración de aplicaciones (default + env + usuario)
- Pipeline de procesamiento con diccionarios de parámetros
- Sobre escritura de settings en tests
- Mantener diccionarios originales sin merge manual
"""

# Ejemplo: configuración de pipeline
pipeline_config = ChainMap({"batch_size": 32}, {"batch_size": 64, "shuffle": True})
print("Pipeline config efectiva:", pipeline_config)


# ------------------------------------------------------------
# 4. MÉTODOS ÚTILES
# ------------------------------------------------------------

# maps → lista de dicts subyacentes
print("Diccionarios subyacentes:", config.maps)

# new_child() → crea un nuevo dict en primer nivel
child_config = config.new_child({"retry": 3})
print("Nuevo child:", child_config)
print("Original unchanged:", config.maps)


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Fusionar dicts manualmente cada vez → pierde eficiencia y claridad
❌ Modificar dicts en niveles incorrectos
❌ Confundir el orden: primero dict = primer nivel de escritura
"""

# ✔ Correcto
cm = ChainMap({"a":1}, {"a":2, "b":3})
print("ChainMap correcto:", cm)
cm["a"] = 10  # modifica primer dict


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Prefiere ChainMap para composición de diccionarios
✔ Documenta la fuente de cada nivel (default, env, user)
✔ Evita merges innecesarios y pérdidas de datos
✔ Usa new_child para cambios temporales
✔ Mantén el orden claro: primer dict = nivel de escritura
"""

print("collections.ChainMap dominado profesionalmente")
