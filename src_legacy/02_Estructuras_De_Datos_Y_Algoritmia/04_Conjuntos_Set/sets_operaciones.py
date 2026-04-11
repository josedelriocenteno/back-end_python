# sets_operaciones.py
"""
OPERACIONES CONJUNTAS CON SETS
================================

Objetivo:
- Dominar unión, intersección, diferencia y diferencias simétricas
- Aplicar operaciones en problemas reales de backend y data
- Uso de métodos y operadores
"""

# ------------------------------------------------------------
# 1. CREACIÓN DE SETS
# ------------------------------------------------------------

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print("Set a:", a)
print("Set b:", b)


# ------------------------------------------------------------
# 2. UNIÓN
# ------------------------------------------------------------

# Operador |
union_op = a | b
print("Unión con | :", union_op)  # {1,2,3,4,5,6}

# Método union()
union_met = a.union(b)
print("Unión con union():", union_met)


# ------------------------------------------------------------
# 3. INTERSECCIÓN
# ------------------------------------------------------------

# Operador &
interseccion_op = a & b
print("Intersección con & :", interseccion_op)  # {3,4}

# Método intersection()
interseccion_met = a.intersection(b)
print("Intersección con intersection():", interseccion_met)


# ------------------------------------------------------------
# 4. DIFERENCIA
# ------------------------------------------------------------

# Elementos en a pero no en b
diferencia_op = a - b
print("Diferencia a - b:", diferencia_op)  # {1,2}

# Método difference()
diferencia_met = a.difference(b)
print("Diferencia con difference():", diferencia_met)


# ------------------------------------------------------------
# 5. DIFERENCIA SIMÉTRICA
# ------------------------------------------------------------

# Elementos en a o b pero no en ambos
diferencia_sim_op = a ^ b
print("Diferencia simétrica ^ :", diferencia_sim_op)  # {1,2,5,6}

# Método symmetric_difference()
diferencia_sim_met = a.symmetric_difference(b)
print("Diferencia simétrica con method:", diferencia_sim_met)


# ------------------------------------------------------------
# 6. OPERACIONES MULTI-SETS
# ------------------------------------------------------------

c = {4, 5, 6, 7}

# Unión múltiple
union_multi = a.union(b, c)
print("Unión múltiple:", union_multi)  # {1,2,3,4,5,6,7}

# Intersección múltiple
inter_multi = a.intersection(b, c)
print("Intersección múltiple:", inter_multi)  # {4}


# ------------------------------------------------------------
# 7. OTROS MÉTODOS ÚTILES
# ------------------------------------------------------------

s = {1,2,3}

print("Está a en s?", 1 in s)     # True
print("Está 4 en s?", 4 in s)     # False
print("Tamaño del set:", len(s))  # 3
s.clear()                          # Vacía el set
print("Después de clear():", s)


# ------------------------------------------------------------
# 8. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Depender del orden de los elementos
❌ Mezclar tipos mutables como elementos
❌ No usar los métodos optimizados y usar loops manuales
"""

# ❌ Elemento mutable
# s = {[1,2]}  # TypeError

# ✔ Tuple inmutable
s = {(1,2)}
print(s)


# ------------------------------------------------------------
# 9. BUENAS PRÁCTICAS
# ------------------------------------------------------------

"""
✔ Prefiere operadores |, &, -, ^ para operaciones claras y rápidas
✔ Usa métodos solo cuando necesites compatibilidad explícita
✔ Documenta qué representa cada set
✔ Evita modificar mientras iteras
✔ Combina sets para filtros y membership tests en pipelines
"""

print("Operaciones con sets dominadas")
