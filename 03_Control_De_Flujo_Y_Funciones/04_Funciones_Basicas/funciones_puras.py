# funciones_puras.py
"""
FUNCIONES PURAS EN PYTHON
=========================

Objetivo:
- Comprender funciones puras: deterministas y sin efectos secundarios
- Saber cuándo y por qué usarlas en backend, pipelines y ML
- Facilitar testing y reproducibilidad
"""

# =========================================================
# 1. Definición de función pura
# =========================================================

def suma(a, b):
    """Devuelve la suma de dos números sin modificar nada externo"""
    return a + b

print(suma(3, 5))  # 8

# =========================================================
# 2. Características de funciones puras
# =========================================================

# ✅ Determinista: siempre devuelve lo mismo para los mismos inputs
# ✅ No tiene efectos secundarios: no modifica variables externas, archivos ni imprime

# Ejemplo impuro (NO recomendable)
contador = 0
def incrementar_contador():
    global contador
    contador += 1
    return contador

# Cada llamada cambia el estado externo → no es pura

# =========================================================
# 3. Funciones puras con estructuras de datos
# =========================================================

def duplicar_lista(lista):
    """Devuelve una nueva lista con valores duplicados, sin modificar la original"""
    return [x*2 for x in lista]

original = [1,2,3]
duplicada = duplicar_lista(original)
print("Original:", original)    # [1,2,3]
print("Duplicada:", duplicada)  # [2,4,6]

# =========================================================
# 4. Funciones puras y ML
# =========================================================

# En pipelines de Machine Learning:
# - Transformaciones de features deben ser puras
# - Permiten reproducibilidad, testing y caching
def normalizar(lista):
    max_val = max(lista)
    return [x/max_val for x in lista]

print(normalizar([1,2,3]))  # [0.333, 0.666, 1.0]

# =========================================================
# 5. Buenas prácticas
# =========================================================

# - Siempre que sea posible, separar lógica pura de efectos secundarios
# - Mantener funciones pequeñas y con responsabilidad única
# - Documentar claramente inputs y outputs
# - Facilita pruebas unitarias y debugging
