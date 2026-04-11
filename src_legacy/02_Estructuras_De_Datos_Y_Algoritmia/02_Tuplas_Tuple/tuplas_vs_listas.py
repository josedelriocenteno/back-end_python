# tuplas_vs_listas.py
"""
TUPLAS VS LISTAS — DECISIONES DE DISEÑO
=====================================

Elegir entre tuple y list NO es estética.
Es una decisión de:
- Diseño
- Seguridad
- Intención
- Mantenibilidad
"""

# ------------------------------------------------------------
# 1. DIFERENCIAS FUNDAMENTALES
# ------------------------------------------------------------

"""
LISTA:
- Mutable
- Pensada para cambiar
- Más flexible
- Más propensa a bugs

TUPLA:
- Inmutable
- Pensada para representar hechos
- Más segura
- Más expresiva semánticamente
"""


# ------------------------------------------------------------
# 2. REGLA DE ORO
# ------------------------------------------------------------

"""
Si NO necesitas modificarlo → TUPLA
Si necesitas modificarlo     → LISTA
"""

# EJEMPLOS

# ✔ Bien
config_db = ("localhost", 5432, "app_db")

# ❌ Mal
config_db_mal = ["localhost", 5432, "app_db"]


# ------------------------------------------------------------
# 3. CASOS REALES EN BACKEND
# ------------------------------------------------------------

# Coordenadas, rangos, pares fijos
punto = (10, 20)

# Resultado de funciones
def get_user():
    return "id_1", "Juan", True

user_id, name, active = get_user()

# Estados permitidos
ESTADOS = ("CREADO", "PAGADO", "ENVIADO")


# ------------------------------------------------------------
# 4. CASOS REALES EN DATA ENGINEERING
# ------------------------------------------------------------

# Filas de un dataset
row = ("2025-01-01", "user_1", 150.5)

# Esquemas fijos
schema = ("id", "timestamp", "value")

# Ventanas de tiempo
window = (start_time, end_time) if False else None


# ------------------------------------------------------------
# 5. LISTAS CUANDO EL CONTENIDO CAMBIA
# ------------------------------------------------------------

# Acumuladores
resultados = []

for i in range(5):
    resultados.append(i)

# Buffers
buffer = []

# Carritos, colas temporales, etc.


# ------------------------------------------------------------
# 6. SEGURIDAD Y BUGS
# ------------------------------------------------------------

"""
Usar tuplas:
✔ Evita modificaciones accidentales
✔ Hace explícito que algo es constante
✔ Reduce efectos colaterales

Muchos bugs vienen de mutar listas
que no deberían mutarse.
"""


# ------------------------------------------------------------
# 7. RENDIMIENTO (NO EXAGERAR)
# ------------------------------------------------------------

"""
✔ Tuplas ocupan un poco menos de memoria
✔ Son ligeramente más rápidas de crear

❌ La diferencia no suele ser crítica
✔ La claridad sí lo es
"""


# ------------------------------------------------------------
# 8. USO COMO CLAVES
# ------------------------------------------------------------

# ✔ Funciona
cache = {}
key = ("user_1", "2025-01-01")
cache[key] = "resultado"

# ❌ No funciona
# key = ["user_1", "2025-01-01"]  # TypeError


# ------------------------------------------------------------
# 9. SEÑALES DE MAL DISEÑO
# ------------------------------------------------------------

"""
🚩 Lista que nunca se modifica
🚩 Configuraciones en listas
🚩 Valores de retorno mutables sin necesidad
"""


# ------------------------------------------------------------
# 10. RESUMEN PROFESIONAL
# ------------------------------------------------------------

"""
TUPLA:
✔ Datos fijos
✔ Contratos
✔ Retornos
✔ Claves

LISTA:
✔ Procesos
✔ Acumulación
✔ Transformación
"""

print("Decisión tuple vs list dominada")
