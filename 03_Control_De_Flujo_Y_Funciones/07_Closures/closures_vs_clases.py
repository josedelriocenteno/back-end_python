# closures_vs_clases.py
"""
CLOSURES VS CLASES EN PYTHON
============================

Objetivo:
- Entender cuándo usar closures y cuándo clases
- Mejorar diseño de funciones y módulos en backend/data pipelines
- Mantener código limpio, testable y modular
"""

# =========================================================
# 1. Caso típico: mantener estado
# =========================================================

# Closure para contador
def contador_closure():
    n = 0
    def incrementar():
        nonlocal n
        n += 1
        return n
    return incrementar

c = contador_closure()
print(c())  # 1
print(c())  # 2

# Clase equivalente
class ContadorClase:
    def __init__(self):
        self.n = 0

    def incrementar(self):
        self.n += 1
        return self.n

c2 = ContadorClase()
print(c2.incrementar())  # 1
print(c2.incrementar())  # 2

# =========================================================
# 2. Comparación práctica
# =========================================================
# Ventajas de closures:
# - Menos código para estados simples
# - No necesitas definir una clase completa
# - Buen para funciones factory, logging, validadores

# Ventajas de clases:
# - Mejor escalabilidad y claridad si hay múltiples métodos
# - Facilitan herencia y composición
# - Ideal si el estado es complejo o mutable en muchos puntos

# =========================================================
# 3. Ejemplo backend: logging de pipeline
# =========================================================

# Closure
def logger_closure(stage_name):
    count = 0
    def log(data):
        nonlocal count
        count += 1
        print(f"[{stage_name}] #{count}: {data}")
        return data
    return log

logger_a = logger_closure("Stage A")
logger_a({"id": 1})  # [Stage A] #1: {'id': 1}

# Clase equivalente
class LoggerStage:
    def __init__(self, stage_name):
        self.stage_name = stage_name
        self.count = 0

    def log(self, data):
        self.count += 1
        print(f"[{self.stage_name}] #{self.count}: {data}")
        return data

logger_b = LoggerStage("Stage B")
logger_b.log({"id": 1})  # [Stage B] #1: {'id': 1}

# =========================================================
# 4. Reglas prácticas para elegir
# =========================================================
# - Estado simple y pocas funciones: usa closure
# - Estado complejo o múltiples métodos: usa clase
# - Necesitas herencia, mixins, composición: usa clase
# - Uso de factories parametrizadas: closure
# - Funciones reutilizables en pipelines: closure

# =========================================================
# 5. Buenas prácticas generales
# =========================================================
# - Documentar qué variables captura un closure
# - Evitar capturar objetos mutables compartidos inadvertidamente
# - No abusar de closures anidadas profundas
# - Mantener la claridad de la API: quien llama debe entender qué recibe
# - Revisar performance si closures se crean muchas veces en bucles pesados
