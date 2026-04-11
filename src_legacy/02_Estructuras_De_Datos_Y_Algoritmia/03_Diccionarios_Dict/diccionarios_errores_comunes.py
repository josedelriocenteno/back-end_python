# diccionarios_errores_comunes.py
"""
ERRORES COMUNES EN EL USO DE DICCIONARIOS
=========================================

Objetivo:
- Evitar bugs típicos en Python
- Entender qué NO hacer
- Aplicar buenas prácticas desde el inicio
"""

# ------------------------------------------------------------
# 1. USAR CLAVES MUTABLES
# ------------------------------------------------------------

# ❌ Esto da TypeError
# dic = {[1,2]: "valor"}

# ✔ Clave válida (inmutable)
dic = {(1,2): "valor"}
print(dic)


# ------------------------------------------------------------
# 2. OLVIDAR KEYERROR
# ------------------------------------------------------------

d = {"a": 1, "b": 2}

# ❌ KeyError si la clave no existe
# print(d["c"])

# ✔ Usar get
print(d.get("c"))          # None
print(d.get("c", 0))       # default


# ------------------------------------------------------------
# 3. MODIFICAR DICCIONARIO MIENTRAS ITERAS
# ------------------------------------------------------------

d = {"a":1, "b":2, "c":3}

# ❌ Iterar y modificar a la vez rompe la iteración
# for k in d:
#     d[k+"_nuevo"] = d[k]

# ✔ Iterar sobre copia de claves
for k in list(d.keys()):
    d[k+"_nuevo"] = d[k]

print(d)


# ------------------------------------------------------------
# 4. USAR CLAVES DUPLICADAS
# ------------------------------------------------------------

dic = {"a":1, "a":2}  # última clave sobreescribe
print(dic)  # {'a':2}


# ------------------------------------------------------------
# 5. NO DOCUMENTAR LA ESTRUCTURA
# ------------------------------------------------------------

"""
Diccionarios anidados complejos sin documentación → confusión y bugs
"""

db = {
    "usuarios": {"user_1": {"nombre":"Juan", "edad":30}},
    "config": {"debug": True}
}

# Mejor documentar:
# db["usuarios"]["user_id"]["campo"]


# ------------------------------------------------------------
# 6. CLAVES QUE NO SON HASHABLES
# ------------------------------------------------------------

# ❌ lista como clave
# d = {["x"]: 1}

# ✔ tuple inmutable
d = {(1,2): "ok"}


# ------------------------------------------------------------
# 7. REEMPLAZO INVOLUNTARIO DE VALORES
# ------------------------------------------------------------

d = {"a":1}
d["a"] = 100  # sobreescribe valor
print(d)


# ------------------------------------------------------------
# 8. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Claves inmutables
✔ Evitar mutar mientras iteras
✔ Documentar estructura
✔ Usar get() o defaultdict para valores opcionales
✔ Evitar sobrescribir claves accidentalmente
✔ Mantener diccionarios pequeños y manejables
"""

from collections import defaultdict

# Ejemplo profesional: contador seguro
logs = ["login","logout","login"]
contador = defaultdict(int)
for log in logs:
    contador[log] += 1

print(contador)

print("Errores comunes de diccionarios dominados")
