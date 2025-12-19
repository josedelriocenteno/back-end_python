# diccionarios_basico.py
"""
DICCIONARIOS EN PYTHON — FUNDAMENTOS PROFESIONALES
==================================================

Diccionarios = Estructura clave en Python:
- Claves → únicas, hashables
- Valores → cualquier objeto
- Acceso → O(1) promedio
- Muy usados en backend, APIs y data pipelines
"""

# ------------------------------------------------------------
# 1. CREACIÓN DE DICCIONARIOS
# ------------------------------------------------------------

# Forma clásica
usuario = {"id": "user_1", "nombre": "Juan", "activo": True}

# Forma con constructor
usuario2 = dict(id="user_2", nombre="Ana", activo=False)

# Diccionario vacío
vacio = {}

print(usuario)
print(usuario2)
print(vacio)


# ------------------------------------------------------------
# 2. ACCESO A ELEMENTOS
# ------------------------------------------------------------

print(usuario["nombre"])     # directo
print(usuario.get("email"))  # devuelve None si no existe
print(usuario.get("email", "no definido"))  # default


# ------------------------------------------------------------
# 3. MODIFICACIÓN Y AGREGADO
# ------------------------------------------------------------

usuario["nombre"] = "Pedro"   # modificar existente
usuario["email"] = "juan@mail.com"  # agregar nuevo

print(usuario)


# ------------------------------------------------------------
# 4. ELIMINACIÓN
# ------------------------------------------------------------

# pop devuelve el valor eliminado
email = usuario.pop("email")
print(email)

# del elimina sin retorno
del usuario["activo"]

print(usuario)


# ------------------------------------------------------------
# 5. ITERACIÓN EFICIENTE
# ------------------------------------------------------------

# Iterar por claves
for key in usuario:
    print(key, usuario[key])

# Iterar por items
for k, v in usuario.items():
    print(k, v)

# Iterar por valores
for v in usuario.values():
    print(v)


# ------------------------------------------------------------
# 6. MÉTODOS IMPORTANTES
# ------------------------------------------------------------

# keys(), values(), items()
print(list(usuario.keys()))
print(list(usuario.values()))
print(list(usuario.items()))

# update() → fusionar diccionarios
usuario.update({"activo": True, "pais": "ES"})
print(usuario)


# ------------------------------------------------------------
# 7. CREAR DICCIONARIOS CON DEFAULTS
# ------------------------------------------------------------

# fromkeys → todas las claves con mismo valor
campos = ["id", "nombre", "email"]
nuevo_usuario = dict.fromkeys(campos, None)
print(nuevo_usuario)


# ------------------------------------------------------------
# 8. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar claves mutables (listas)
❌ Olvidar manejar KeyError
❌ Iterar y modificar al mismo tiempo
❌ No documentar la estructura
"""

# Clave mutable ❌
# dic = {[1,2]: "valor"}  # TypeError

# Iterar y modificar ❌
dic = {"a":1, "b":2}
for k in dic: 
    # dic[k+"nuevo"] = dic[k]  # ❌ rompe la iteración
    pass


# ------------------------------------------------------------
# 9. DICCIONARIOS ANIDADOS
# ------------------------------------------------------------

db = {
    "usuarios": {"user_1": {"nombre":"Juan"}, "user_2":{"nombre":"Ana"}},
    "config": {"debug": True}
}

print(db["usuarios"]["user_1"]["nombre"])


# ------------------------------------------------------------
# 10. CASOS REALES EN BACKEND
# ------------------------------------------------------------

"""
✔ Representar objetos JSON
✔ Acumular resultados intermedios
✔ Contadores y lookup tables
✔ Mapear claves de caches
"""

# Contador simple
resultados = {}
for i in ["a","b","a","a","b"]:
    resultados[i] = resultados.get(i,0) + 1

print(resultados)


# ------------------------------------------------------------
# 11. SEÑALES DE BUEN USO
# ------------------------------------------------------------

"""
✔ Claves claras y únicas
✔ Acceso seguro con get
✔ Diccionarios pequeños y manejables
✔ Anidar con sentido
"""

print("Diccionarios básicos dominados")
