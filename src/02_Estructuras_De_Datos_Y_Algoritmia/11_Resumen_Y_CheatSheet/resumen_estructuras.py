# resumen_estructuras.py
"""
RESUMEN PROFESIONAL – ESTRUCTURAS DE DATOS EN PYTHON
===================================================

Este archivo NO enseña desde cero.
Sirve para:
- Repasar rápido
- Reforzar criterio
- Recordar por qué se elige cada estructura

Si no entiendes algo aquí, vuelve a la unidad.
"""

# =========================================================
# CONCEPTOS BASE
# =========================================================

"""
Una estructura de datos define:
- Cómo se almacenan los datos
- Cómo se accede a ellos
- Qué operaciones son eficientes
"""

"""
Regla de oro:
→ La estructura correcta simplifica el código
→ La estructura incorrecta crea bugs y cuellos de botella
"""

# =========================================================
# LIST (list)
# =========================================================

"""
Cuándo usar:
- Datos ordenados
- Iteración secuencial
- Tamaño variable
- Acceso por índice

Costes:
- Acceso por índice: O(1)
- append: O(1) amortizado
- insert / pop(0): O(n)

Errores comunes:
- Usar list como cola
- Buscar pertenencia en listas grandes
- Copiar listas sin entender referencias
"""

# =========================================================
# TUPLE (tuple)
# =========================================================

"""
Cuándo usar:
- Datos inmutables
- Claves de dict
- Retornos múltiples
- Seguridad contra modificaciones

Ventajas:
- Más ligera que list
- Hashable
- Expresa intención

Error típico:
- Usarla como lista mutable
"""

# =========================================================
# SET (set)
# =========================================================

"""
Cuándo usar:
- Eliminar duplicados
- Membership test rápido
- Operaciones matemáticas de conjuntos

Costes:
- Búsqueda: O(1)
- Inserción: O(1)

Errores comunes:
- Asumir orden
- Usar para datos que necesitan índice
- Meter elementos mutables
"""

# =========================================================
# DICT (dict)
# =========================================================

"""
Cuándo usar:
- Lookup rápido por clave
- Representar entidades
- Contadores y agrupaciones
- Cacheo

Costes:
- Acceso: O(1)
- Inserción: O(1)

Errores graves:
- Claves mutables
- Abusar de dicts anidados sin control
- Usarlo cuando una estructura simple basta
"""

# =========================================================
# STACK (PILA)
# =========================================================

"""
LIFO (Last In, First Out)

Usos reales:
- Undo / Redo
- Backtracking
- Evaluación de expresiones

Implementación recomendada:
- list (append / pop)
"""

# =========================================================
# QUEUE (COLA)
# =========================================================

"""
FIFO (First In, First Out)

Usos reales:
- Procesamiento de tareas
- Requests
- Buffers

Implementación correcta:
- collections.deque

Error crítico:
- Usar list con pop(0)
"""

# =========================================================
# PRIORITY QUEUE
# =========================================================

"""
Usos reales:
- Scheduling
- Sistemas de prioridades
- Optimización de recursos

Implementación:
- heapq

Error común:
- Usarla cuando FIFO es suficiente
"""

# =========================================================
# ESTRUCTURAS AVANZADAS (collections)
# =========================================================

"""
Counter:
- Conteos eficientes

defaultdict:
- Inicialización automática

namedtuple:
- Datos estructurados ligeros

ChainMap:
- Composición de configuraciones
"""

# =========================================================
# COMPLEJIDAD Y RENDIMIENTO
# =========================================================

"""
Big-O no es teoría:
- Es coste real
- Impacta escalabilidad
- Define arquitectura

Regla:
→ Si algo escala mal con datos pequeños, explotará con datos grandes
"""

# =========================================================
# BACKEND Y DATA ENGINEERING
# =========================================================

"""
Backend:
- dict para entidades
- set para validaciones
- queue para requests

Data Engineering:
- list para batches
- dict para agregaciones
- deque para ventanas
"""

# =========================================================
# CRITERIO FINAL
# =========================================================

"""
Antes de escribir código, pregúntate:
1. ¿Necesito orden?
2. ¿Necesito acceso rápido?
3. ¿Necesito unicidad?
4. ¿Voy a escalar?
"""

"""
Cambiar estructura > optimizar microcódigo
"""

print("Resumen de estructuras dominado")
