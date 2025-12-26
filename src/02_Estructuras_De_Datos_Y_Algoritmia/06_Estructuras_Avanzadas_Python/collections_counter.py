# collections_counter.py
"""
COLLECTIONS.COUNTER EN PYTHON — CONTEO EFICIENTE
=================================================

Objetivo:
- Usar Counter para contar elementos de manera eficiente
- Aplicaciones en backend, análisis de datos y pipelines
- Operaciones avanzadas con conteos
"""

from collections import Counter

# ------------------------------------------------------------
# 1. CREACIÓN DE UN COUNTER
# ------------------------------------------------------------

# A partir de lista
frutas = ["manzana", "banana", "manzana", "naranja", "banana", "manzana"]
conteo_frutas = Counter(frutas)
print("Conteo de frutas:", conteo_frutas)

# A partir de string
texto = "abracadabra"
conteo_letras = Counter(texto)
print("Conteo de letras:", conteo_letras)

# A partir de diccionario
conteo_dic = Counter({"a": 3, "b": 1})
print("Counter desde diccionario:", conteo_dic)


# ------------------------------------------------------------
# 2. ACCESO Y OPERACIONES BÁSICAS
# ------------------------------------------------------------

# Acceso a un elemento
print("Cantidad de manzanas:", conteo_frutas["manzana"])

# Elemento no existente → 0
print("Cantidad de peras:", conteo_frutas["pera"])

# Suma y resta de counters
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print("Suma:", c1 + c2)
print("Resta:", c1 - c2)  # elimina negativos

# Operaciones con elementos comunes
print("Intersección:", c1 & c2)
print("Unión:", c1 | c2)


# ------------------------------------------------------------
# 3. MÉTODOS ÚTILES
# ------------------------------------------------------------

# Most common
print("Más comunes 2:", conteo_frutas.most_common(2))

# Update: añadir más elementos
conteo_frutas.update(["banana", "pera", "pera"])
print("Después de update:", conteo_frutas)

# Subtract: restar elementos
conteo_frutas.subtract(["manzana", "naranja"])
print("Después de subtract:", conteo_frutas)


# ------------------------------------------------------------
# 4. USOS COMUNES EN BACKEND / DATA
# ------------------------------------------------------------

"""
- Contar logs: requests por endpoint, códigos de estado
- Contar elementos únicos en pipelines
- Encontrar palabras más frecuentes en texto
- Analítica de datos rápida
"""

# Ejemplo: conteo de requests por endpoint
requests = ["/login", "/home", "/login", "/profile", "/home", "/login"]
conteo_requests = Counter(requests)
print("Requests por endpoint:", conteo_requests)


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar diccionario manual para conteo → más código, más propenso a errores
❌ Restar elementos sin manejar negativos → errores de lógica
❌ Confundir update con assign
"""

# ✔ Correcto
c = Counter()
c.update(["x","y","x"])
print(c)


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Prefiere Counter para conteos frecuentes
✔ Usa most_common() para top-N
✔ Documenta qué se está contando
✔ Evita modificar manualmente el diccionario interno
✔ Combine Counter con lógica de filtrado si es necesario
"""

print("collections.Counter dominado profesionalmente")
