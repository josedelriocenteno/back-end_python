# estructuras_para_sql.py
"""
ESTRUCTURAS DE DATOS PARA SQL → PYTHON — BACKEND/DATA PROFESIONAL
=================================================================

Objetivo:
- Mapear resultados de consultas SQL a estructuras Python adecuadas
- Elegir la estructura según uso: acceso rápido, orden, agregaciones
- Optimizar performance y legibilidad de código
"""

# ------------------------------------------------------------
# 1. LISTAS PARA FILAS ORDENADAS
# ------------------------------------------------------------

# SQL retorna filas ordenadas → lista de tuplas o dicts
resultados_sql = [
    (1, "Alice", 30),
    (2, "Bob", 25),
    (3, "Carol", 35)
]

# Acceso secuencial o indexado
for fila in resultados_sql:
    id_, nombre, edad = fila
    print(f"{nombre} tiene {edad} años")

# Uso típico en endpoints o procesamiento por orden


# ------------------------------------------------------------
# 2. DICCIONARIOS PARA ACCESO POR CLAVE
# ------------------------------------------------------------

# Mapear columnas a nombres → acceso rápido por columna
resultados_dict = [
    {"id": 1, "nombre": "Alice", "edad": 30},
    {"id": 2, "nombre": "Bob", "edad": 25},
    {"id": 3, "nombre": "Carol", "edad": 35}
]

# Ejemplo: obtener edad de Bob
edad_bob = next((r["edad"] for r in resultados_dict if r["nombre"] == "Bob"), None)
print("Edad de Bob:", edad_bob)


# ------------------------------------------------------------
# 3. DICCIONARIO DE DICCIONARIOS PARA LOOKUPS RÁPIDOS
# ------------------------------------------------------------

# Si consultas frecuentes por id → dict[id] = fila
lookup_por_id = {r["id"]: r for r in resultados_dict}
print("Lookup id=2:", lookup_por_id[2])


# ------------------------------------------------------------
# 4. SETS PARA VALORES ÚNICOS
# ------------------------------------------------------------

# Evitar duplicados o membership test rápido
edades_unicas = {r["edad"] for r in resultados_dict}
print("Edades únicas:", edades_unicas)


# ------------------------------------------------------------
# 5. PANDAS PARA DATA ENGINEERING / ML
# ------------------------------------------------------------

import pandas as pd

df = pd.DataFrame(resultados_dict)
print("DataFrame completo:\n", df)

# Acceso eficiente por columna
print("Nombres:", df["nombre"].tolist())
# Filtrado
df_mayores_30 = df[df["edad"] > 30]
print("Mayores de 30:\n", df_mayores_30)


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usa listas para iteración ordenada y endpoints simples
✔ Usa diccionarios para lookup rápido y JSON responses
✔ Usa dict[id] = fila si consultas frecuentes por clave
✔ Usa sets para membership test o valores únicos
✔ Prefiere Pandas cuando trabajes con datasets grandes o pipelines ML
✔ Documenta claramente el tipo de retorno de cada query
✔ No cargues todo en memoria si dataset es gigante → usar generadores / chunks
"""

print("Mapeo SQL → Python dominado profesionalmente")
