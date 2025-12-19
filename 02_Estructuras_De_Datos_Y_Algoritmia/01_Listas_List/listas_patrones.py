# listas_patrones.py
"""
PATRONES DE USO DE LISTAS EN PYTHON
==================================

Las listas no se usan “porque sí”.
En backend y data se usan siguiendo PATRONES claros.

Este archivo cubre:
- Stack (pila)
- Buffer
- Acumulador
- Casos reales de uso profesional
"""

# ------------------------------------------------------------
# 1. LISTA COMO STACK (PILA)
# ------------------------------------------------------------

"""
Stack = LIFO (Last In, First Out)

Operaciones:
- push → append()
- pop  → pop()

Coste:
- append() → O(1) amortizado
- pop()    → O(1)

✔ Uso recomendado
"""

stack = []

# push
stack.append("a")
stack.append("b")
stack.append("c")

# pop
ultimo = stack.pop()

print("Stack:", stack)
print("Elemento sacado:", ultimo)


# ------------------------------------------------------------
# 2. ERRORES COMUNES CON STACK
# ------------------------------------------------------------

"""
❌ Usar insert(0, x)
❌ Usar pop(0)

Eso rompe el patrón y el rendimiento.
"""


# ------------------------------------------------------------
# 3. LISTA COMO BUFFER (DATOS TEMPORALES)
# ------------------------------------------------------------

"""
Buffer = almacén temporal de datos
Muy común en:
- Lectura de archivos
- Procesamiento por lotes
- Pipelines de datos
"""

buffer = []
BATCH_SIZE = 3

datos_entrada = [1, 2, 3, 4, 5, 6, 7]

for dato in datos_entrada:
    buffer.append(dato)

    if len(buffer) == BATCH_SIZE:
        print("Procesando batch:", buffer)
        buffer.clear()  # O(n) pero pequeño y controlado

# Procesar resto
if buffer:
    print("Procesando batch final:", buffer)


# ------------------------------------------------------------
# 4. BUFFER MAL IMPLEMENTADO (ANTI-PATRÓN)
# ------------------------------------------------------------

"""
❌ Hacer pop(0) repetidamente
❌ Dejar crecer el buffer sin límite
❌ Copiar el buffer innecesariamente
"""


# ------------------------------------------------------------
# 5. LISTA COMO ACUMULADOR
# ------------------------------------------------------------

"""
Acumulador = ir juntando resultados

Patrón extremadamente común:
- Recolectar respuestas
- Construir payloads
- Agregar resultados parciales
"""

resultados = []

for i in range(5):
    resultados.append(i * i)

print("Resultados acumulados:", resultados)


# ------------------------------------------------------------
# 6. ACUMULADOR VS CONCATENACIÓN
# ------------------------------------------------------------

"""
❌ MAL:
resultados = resultados + [nuevo]

✔ BIEN:
resultados.append(nuevo)

La concatenación crea una lista nueva → O(n)
append modifica in-place → O(1)
"""


# ------------------------------------------------------------
# 7. LISTAS COMO COLAS — CUÁNDO NO USARLAS
# ------------------------------------------------------------

"""
Cola = FIFO (First In, First Out)

❌ Usar lista:
- append()
- pop(0) → O(n)

✔ Usar collections.deque
"""

from collections import deque

cola = deque()

cola.append("task1")
cola.append("task2")

tarea = cola.popleft()

print("Tarea procesada:", tarea)


# ------------------------------------------------------------
# 8. LISTA COMO HISTORIAL / LOG SIMPLE
# ------------------------------------------------------------

"""
Uso frecuente:
- Historial de eventos
- Cambios recientes
- Estados intermedios
"""

historial = []

def registrar_evento(evento):
    historial.append(evento)

registrar_evento("inicio")
registrar_evento("procesando")
registrar_evento("fin")

print("Historial:", historial)


# ------------------------------------------------------------
# 9. PATRÓN MAP + ACUMULADOR
# ------------------------------------------------------------

datos = [1, 2, 3, 4]

procesados = []

for x in datos:
    procesados.append(x * 10)

# Alternativa:
procesados = [x * 10 for x in datos]


# ------------------------------------------------------------
# 10. LISTAS EN BACKEND REAL
# ------------------------------------------------------------

"""
Casos reales:
✔ Lista de DTOs antes de serializar a JSON
✔ Acumulador de resultados SQL
✔ Buffer de eventos antes de enviar a otro servicio
✔ Stack para parsing o validaciones
"""


# ------------------------------------------------------------
# 11. REGLAS DE ORO
# ------------------------------------------------------------

"""
✔ append y pop() final siempre que puedas
✔ listas pequeñas y controladas
✔ si cambia el patrón → cambia la estructura
✔ lista no es comodín universal
"""

print("Patrones de listas dominados")
