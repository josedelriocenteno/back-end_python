# nested_comprehensions.py
"""
COMPREHENSIONS ANIDADAS EN PYTHON
=================================

Objetivo:
- Entender cómo funcionan las comprensiones anidadas
- Saber cuándo NO usarlas por legibilidad y mantenimiento
- Aplicable a backend, pipelines y transformación de datos
"""

# =========================================================
# 1. Ejemplo básico
# =========================================================

# Crear una matriz 3x3
matriz = [[i * j for j in range(3)] for i in range(3)]
print(matriz)  # [[0,0,0],[0,1,2],[0,2,4]]

# =========================================================
# 2. Comprensión anidada con condición
# =========================================================

# Filtrar solo productos pares
pares = [[i * j for j in range(3) if (i*j) % 2 == 0] for i in range(3)]
print(pares)  # [[0,0,0],[0,2],[0,2,4]]

# =========================================================
# 3. Problemas de legibilidad
# =========================================================

# ❌ Evitar comprensiones muy largas o con múltiples condiciones
# resultado = [[(i+j)**2 if i%2==0 else i-j for j in range(5)] for i in range(5)]

# ✅ Mejor descomponer en bucles claros
resultado = []
for i in range(5):
    fila = []
    for j in range(5):
        if i % 2 == 0:
            fila.append((i+j)**2)
        else:
            fila.append(i-j)
    resultado.append(fila)

# =========================================================
# 4. Buenas prácticas
# =========================================================

# - Usa nested comprehensions solo para matrices simples
# - Prefiere bucles explícitos si la lógica es compleja
# - Mantén legibilidad profesional: otros devs deben entenderlo rápido
# - Documenta la intención con comentarios claros

# =========================================================
# 5. Aplicación profesional
# =========================================================

# Backend/data: preparación de batches, creación de tablas en memoria
usuarios = [
    {"nombre": "Ana", "edades": [25, 26]},
    {"nombre": "Luis", "edades": [17, 18]},
    {"nombre": "Marta", "edades": [30, 31]}
]

# Extraer todos los años mayores de edad
mayores = [edad for u in usuarios for edad in u["edades"] if edad >= 18]
print(mayores)  # [25, 26, 18, 30, 31]
