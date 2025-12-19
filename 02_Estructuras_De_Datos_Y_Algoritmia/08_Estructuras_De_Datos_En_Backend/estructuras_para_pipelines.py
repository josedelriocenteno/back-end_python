# estructuras_para_pipelines.py
"""
ESTRUCTURAS DE DATOS PARA PIPELINES — BACKEND Y DATA PROFESIONAL
================================================================

Objetivo:
- Elegir estructuras adecuadas para pipelines y procesamiento de datos
- Manejar acumuladores, buffers y batches de manera eficiente
- Evitar cuellos de botella y consumo excesivo de memoria
"""

# ------------------------------------------------------------
# 1. ACUMULADORES
# ------------------------------------------------------------

# Útiles para:
# - Sumar, contar, agregar resultados durante iteración
# - Estadísticas simples en tiempo real

numeros = [1, 2, 3, 4, 5]
suma_total = 0
for n in numeros:
    suma_total += n  # acumulador O(n)
print("Suma total:", suma_total)

# Para conteos, usar collections.Counter → más eficiente y legible
from collections import Counter
palabras = ["apple", "banana", "apple", "orange"]
contador = Counter(palabras)
print("Conteo palabras:", contador)


# ------------------------------------------------------------
# 2. BUFFERS
# ------------------------------------------------------------

# Útiles para:
# - Almacenar temporalmente datos antes de procesarlos
# - Evitar procesamiento individual innecesario
# - Optimizar I/O en pipelines

buffer = []
def procesar_batch(data):
    print("Procesando batch:", data)

# Simulación de acumulación en buffer
for item in range(10):
    buffer.append(item)
    if len(buffer) >= 5:  # tamaño del batch
        procesar_batch(buffer)
        buffer.clear()  # vaciar buffer

# Resultado: procesamiento eficiente en batches de 5


# ------------------------------------------------------------
# 3. BATCHES
# ------------------------------------------------------------

# Batch processing → procesar datos en grupos
def procesar_lote(lote):
    # simulación de procesamiento
    return [x**2 for x in lote]

datos = list(range(20))
batch_size = 4
for i in range(0, len(datos), batch_size):
    batch = datos[i:i+batch_size]
    resultado = procesar_lote(batch)
    print("Resultado batch:", resultado)


# ------------------------------------------------------------
# 4. GENERADORES PARA EFICIENCIA
# ------------------------------------------------------------

# Generadores evitan cargar todo en memoria
def generar_datos(n):
    for i in range(n):
        yield i

for valor in generar_datos(10):
    print("Generador valor:", valor)

# Útil para pipelines grandes → O(1) memoria por elemento


# ------------------------------------------------------------
# 5. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usa acumuladores para sumas, contadores y agregaciones simples
✔ Usa buffers para procesar datos en batches y optimizar I/O
✔ Evita listas gigantes → usa generadores para memoria eficiente
✔ Determina tamaño de batch según memoria y velocidad de procesamiento
✔ Documenta cada etapa del pipeline (input/output)
✔ Prefiere estructuras nativas (list, deque, Counter) antes que inventar
✔ Mide performance con datasets grandes antes de producción
"""

print("Estructuras para pipelines dominadas profesionalmente")
