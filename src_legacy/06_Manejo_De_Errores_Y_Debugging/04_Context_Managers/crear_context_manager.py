"""
crear_context_manager.py
========================

Objetivo:
- Aprender a implementar context managers propios
- Controlar recursos de forma automática y segura
- Usar __enter__ y __exit__ para inicialización y limpieza
"""

# -------------------------------------------------------------------
# 1️⃣ ESTRUCTURA BÁSICA DE UN CONTEXT MANAGER
# -------------------------------------------------------------------

class Recurso:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.abierto = False

    def __enter__(self):
        """Se ejecuta al entrar al bloque 'with'"""
        print(f"Abriendo recurso {self.nombre}")
        self.abierto = True
        return self  # objeto disponible dentro del bloque

    def __exit__(self, exc_type, exc_value, traceback):
        """Se ejecuta al salir del bloque 'with'"""
        print(f"Cerrando recurso {self.nombre}")
        self.abierto = False
        if exc_type:
            print(f"Ocurrió excepción: {exc_value}")
        # return False → Propaga la excepción fuera del bloque
        return False

# -------------------------------------------------------------------
# 2️⃣ USO DEL CONTEXT MANAGER
# -------------------------------------------------------------------

with Recurso("ArchivoDatos") as r:
    print(f"Recurso abierto: {r.abierto}")
    # Si ocurre un error aquí, __exit__ aún se ejecuta
    # raise ValueError("Error de prueba")

print(f"Recurso abierto después del bloque: {r.abierto}")  # False

# -------------------------------------------------------------------
# 3️⃣ PROTECCIÓN ANTE EXCEPCIONES
# -------------------------------------------------------------------

try:
    with Recurso("ArchivoPrueba") as r:
        raise RuntimeError("Error intencional")
except RuntimeError as e:
    print(f"Excepción capturada fuera del with: {e}")

# Output:
# Abriendo recurso ArchivoPrueba
# Cerrando recurso ArchivoPrueba
# Ocurrió excepción: Error intencional
# Excepción capturada fuera del with: Error intencional

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# 1. __enter__ → inicializa el recurso y devuelve lo que usarás dentro del with
# 2. __exit__ → libera el recurso automáticamente, incluso si hay error
# 3. No suprimir excepciones a menos que sea necesario (return False)
# 4. Logging dentro de __exit__ ayuda a depurar problemas con recursos
# 5. Usar context managers para archivos, conexiones, locks, sesiones, etc.

# -------------------------------------------------------------------
# 5️⃣ RESUMEN
# -------------------------------------------------------------------

# - Context managers reemplazan try/finally manuales
# - __enter__ → setup
# - __exit__ → cleanup
# - Garantiza liberación de recursos incluso si ocurre error
# - Mejora legibilidad, seguridad y mantenibilidad del código
