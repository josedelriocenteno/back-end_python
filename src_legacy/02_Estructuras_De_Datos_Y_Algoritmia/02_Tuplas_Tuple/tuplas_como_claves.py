# tuplas_como_claves.py
"""
TUPLAS COMO CLAVES EN DICTS Y SETS
=================================

Las tuplas son INMUTABLES → por eso pueden ser:
✔ claves de diccionarios
✔ elementos de sets

Esto es fundamental en:
- caches
- índices
- lookup tables
- claves compuestas
"""

# ------------------------------------------------------------
# 1. POR QUÉ LAS LISTAS NO SIRVEN COMO CLAVES
# ------------------------------------------------------------

"""
Las claves en dict y los elementos en set deben ser:
- Inmutables
- Hashables

Las listas son mutables → NO hashables
"""

# key = [1, 2]        # ❌ TypeError
key = (1, 2)          # ✔ Correcto


# ------------------------------------------------------------
# 2. HASHING EXPLICADO SIN HUMO
# ------------------------------------------------------------

"""
Hash:
- Número entero derivado del contenido
- Se usa para localizar datos rápidamente

Si un objeto cambia, su hash cambiaría.
Por eso los mutables no pueden ser claves.
"""

print(hash((1, 2)))
# print(hash([1, 2]))  # ❌ Error


# ------------------------------------------------------------
# 3. TUPLAS COMO CLAVES COMPUESTAS
# ------------------------------------------------------------

"""
Muy común en backend:
Claves formadas por múltiples campos.
"""

cache = {}

cache[("user_1", "2025-01-01")] = "resultado A"
cache[("user_1", "2025-01-02")] = "resultado B"

print(cache[("user_1", "2025-01-01")])


# ------------------------------------------------------------
# 4. EJEMPLO REAL: CACHE DE CONSULTAS
# ------------------------------------------------------------

def obtener_resultado(user_id, fecha):
    clave = (user_id, fecha)

    if clave in cache:
        return cache[clave]

    resultado = f"procesado {user_id} {fecha}"
    cache[clave] = resultado
    return resultado

print(obtener_resultado("user_2", "2025-01-03"))
print(obtener_resultado("user_2", "2025-01-03"))


# ------------------------------------------------------------
# 5. TUPLAS EN SETS
# ------------------------------------------------------------

"""
Un set es básicamente un dict sin valores.
"""

visitas = set()

visitas.add(("user_1", "home"))
visitas.add(("user_1", "home"))  # duplicado, no se añade
visitas.add(("user_2", "login"))

print(visitas)


# ------------------------------------------------------------
# 6. TUPLAS DENTRO DE TUPLAS
# ------------------------------------------------------------

"""
Mientras todos los elementos sean hashables,
la tupla completa lo será.
"""

key = (("user_1", 2025), ("page", "home"))
print(hash(key))


# ------------------------------------------------------------
# 7. ERROR SUTIL: MUTABLES DENTRO DE TUPLAS
# ------------------------------------------------------------

"""
Esto NO es válido como clave,
aunque la tupla sea inmutable.
"""

# clave_mala = (1, [2, 3])  # ❌ TypeError


# ------------------------------------------------------------
# 8. USO EN DATA ENGINEERING
# ------------------------------------------------------------

"""
✔ Claves de ventanas temporales
✔ Agrupaciones (group by)
✔ Identificadores de features
"""

window_key = ("user_1", "2025-01-01", "00:00-01:00")


# ------------------------------------------------------------
# 9. BUENAS PRÁCTICAS
# ------------------------------------------------------------

"""
✔ Usar tuplas para claves compuestas
✔ Mantener las tuplas simples
✔ No meter mutables dentro
✔ Documentar el significado de cada posición
"""


# ------------------------------------------------------------
# 10. SEÑALES DE MAL DISEÑO
# ------------------------------------------------------------

"""
🚩 Claves como strings concatenadas
🚩 Uso de listas donde debería haber tuplas
🚩 Claves mágicas sin estructura
"""

print("Tuplas como claves dominadas")
