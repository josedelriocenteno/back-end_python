# diccionarios_complejidad.py
"""
COMPLEJIDAD DE DICCIONARIOS EN PYTHON
=====================================

Objetivo:
- Entender Big-O en operaciones clave
- Colisiones y resize
- Evitar cuellos de botella en producción

Conceptos:
- Acceso / inserción / eliminación: O(1) promedio
- Iteración: O(n)
- Colisiones → manejo interno (probing)
- Resize → costoso pero infrecuente
"""

# ------------------------------------------------------------
# 1. ACCESO, INSERCIÓN Y ELIMINACIÓN
# ------------------------------------------------------------

d = {}

# Inserción
d["a"] = 1       # O(1) promedio
d["b"] = 2
d["c"] = 3

# Acceso
print(d["b"])    # O(1) promedio

# Eliminación
del d["a"]       # O(1) promedio

# ------------------------------------------------------------
# 2. ITERACIÓN
# ------------------------------------------------------------

# Iterar por keys, values o items → O(n)
for k in d:
    print(k, d[k])

# ------------------------------------------------------------
# 3. COLISIONES
# ------------------------------------------------------------

"""
Dos claves diferentes pueden producir el mismo hash
Python maneja esto internamente mediante probing
El usuario no suele verlo, pero afecta performance si ocurre mucho
"""

# Claves personalizadas con colisiones
class ClaveMala:
    def __init__(self, val):
        self.val = val
    def __hash__(self):
        return 42  # todas las claves colisionan
    def __eq__(self, other):
        return self.val == other.val

d_col = {}
d_col[ClaveMala(1)] = "uno"
d_col[ClaveMala(2)] = "dos"
d_col[ClaveMala(3)] = "tres"

print(d_col)  # funciona, pero internamente más lento

# ------------------------------------------------------------
# 4. REDIMENSIONAMIENTO AUTOMÁTICO
# ------------------------------------------------------------

"""
- Los dicts crecen dinámicamente
- Cuando se alcanza cierto load factor (~2/3)
- Python crea nueva tabla y re-hashea todas las claves
- Coste O(n), pero raro → amortizado a O(1) por operación
"""

# Test de redimensionamiento
big_dict = {}
for i in range(100000):
    big_dict[i] = i*i  # varias reasignaciones internas ocurren

print(len(big_dict))

# ------------------------------------------------------------
# 5. BUENAS PRÁCTICAS
# ------------------------------------------------------------

"""
✔ Prefiere claves inmutables
✔ Evita colisiones artificiales (hash personalizado raro)
✔ No iterar y modificar al mismo tiempo
✔ Ten en cuenta tamaño de dicts muy grandes
✔ Usa dicts para lookups rápidos, no solo para listas con índice
"""

# ------------------------------------------------------------
# 6. RESUMEN BIG-O
# ------------------------------------------------------------

"""
Operación         Complejidad promedio   Peor caso
---------------------------------------------------
Acceso clave      O(1)                 O(n)
Inserción clave   O(1)                 O(n)
Eliminación clave O(1)                 O(n)
Iteración         O(n)                 O(n)
"""

print("Complejidad de diccionarios dominada")
