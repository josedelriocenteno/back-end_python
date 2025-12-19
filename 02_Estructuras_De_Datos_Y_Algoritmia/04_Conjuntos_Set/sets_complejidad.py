# sets_complejidad.py
"""
SETS EN PYTHON — COMPLEJIDAD Y USO EFICIENTE
============================================

Objetivo:
- Comprender costes de operaciones O(1) y O(n)
- Evitar cuellos de botella
- Aplicar sets de manera óptima en backend y data pipelines
"""

# ------------------------------------------------------------
# 1. CREACIÓN DE SETS
# ------------------------------------------------------------

s = set()             # O(1)
s2 = {1, 2, 3, 4}     # O(n) por los elementos iniciales
print(s, s2)


# ------------------------------------------------------------
# 2. ACCESO Y MEMBERSHIP TEST
# ------------------------------------------------------------

s = {1,2,3,4,5}

# Membership test
print(3 in s)  # O(1) promedio
print(10 in s) # O(1) promedio

# Nota: iteración sobre el set → O(n)
for x in s:
    pass


# ------------------------------------------------------------
# 3. OPERACIONES CONJUNTAS
# ------------------------------------------------------------

a = {1,2,3,4}
b = {3,4,5,6}

# Unión O(len(a) + len(b))
union = a | b

# Intersección O(min(len(a), len(b)))
inter = a & b

# Diferencia O(len(a))
diff = a - b

# Diferencia simétrica O(len(a) + len(b))
sym_diff = a ^ b

print(union, inter, diff, sym_diff)


# ------------------------------------------------------------
# 4. ADICIONES Y ELIMINACIONES
# ------------------------------------------------------------

s = set()

# Add O(1) promedio
for i in range(100000):
    s.add(i)

# Remove O(1) promedio
s.remove(50000)

# Discard O(1), no falla si no existe
s.discard(999999)


# ------------------------------------------------------------
# 5. USO EFICIENTE EN BACKEND / DATA
# ------------------------------------------------------------

# Filtrado rápido
usuarios = [1,2,3,4,5,6,7,8,9]
ids_permitidos = {2,4,6,8}
permitidos = [u for u in usuarios if u in ids_permitidos]  # O(len(usuarios))

print(permitidos)

# Eliminación de duplicados
emails = ["a@x.com", "b@x.com", "a@x.com"]
emails_unicos = list(set(emails))
print(emails_unicos)


# ------------------------------------------------------------
# 6. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar listas para membership test → O(n) lento
❌ Iterar y modificar set a la vez
❌ Ignorar coste de operaciones en sets grandes
❌ Usar elementos mutables (list, dict) → TypeError
"""

# ❌ Error clásico
# lista = [1,2,3,4]
# 999 in lista  # O(n)

# ✔ Correcto con set
s = {1,2,3,4}
print(999 in s)  # O(1)


# ------------------------------------------------------------
# 7. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Prefiere sets para membership test O(1)
✔ Usa operadores para unión/intersección/diferencia
✔ Evita loops anidados donde se puede usar set
✔ Elimina duplicados con set()
✔ Documenta claramente qué contiene cada set
✔ Iterar sobre copia si vas a modificar
"""

print("Sets optimizados y complejidad dominada")
