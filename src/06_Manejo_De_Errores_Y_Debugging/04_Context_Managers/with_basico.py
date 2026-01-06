"""
with_basico.py
===============

Objetivo:
- Aprender a usar `with` para manejar recursos (archivos, conexiones, locks)
- Evitar fugas y liberar recursos automáticamente
- Simplificar código y aumentar seguridad
"""

# -------------------------------------------------------------------
# 1️⃣ USO DE WITH CON ARCHIVOS
# -------------------------------------------------------------------

# ❌ Sin with: hay que usar try/finally
try:
    f = open("datos.txt", "r")
    contenido = f.read()
finally:
    f.close()

# ✅ Con with: más limpio y seguro
with open("datos.txt", "r") as f:
    contenido = f.read()
    print(contenido)

# Ventajas:
# - El archivo se cierra automáticamente al salir del bloque
# - Se maneja correctamente incluso si ocurre una excepción
# - Código más legible

# -------------------------------------------------------------------
# 2️⃣ USO DE WITH CON LOCKS
# -------------------------------------------------------------------

import threading

lock = threading.Lock()

# ❌ Sin with
lock.acquire()
try:
    # sección crítica
    print("Sección crítica ejecutada")
finally:
    lock.release()

# ✅ Con with
with lock:
    # sección crítica
    print("Sección crítica ejecutada con with ✅")

# Ventaja:
# - Bloqueo y desbloqueo automáticos
# - Evita deadlocks por olvido de release

# -------------------------------------------------------------------
# 3️⃣ USO DE WITH CON CONEXIONES SIMULADAS
# -------------------------------------------------------------------

class ConexionDB:
    def __init__(self):
        self.abierta = False

    def abrir(self):
        print("Conexión abierta")
        self.abierta = True

    def cerrar(self):
        print("Conexión cerrada")
        self.abierta = False

    # Implementamos métodos para usar with
    def __enter__(self):
        self.abrir()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cerrar()
        # return False → Propaga excepciones si ocurren
        return False

# Uso
with ConexionDB() as db:
    print("Ejecutando queries")
    # Si ocurre error, conexión se cierra automáticamente

# -------------------------------------------------------------------
# 4️⃣ VENTAJAS DEL USO DE WITH
# -------------------------------------------------------------------

# 1. Simplifica manejo de recursos
# 2. Garantiza limpieza aunque haya excepciones
# 3. Reduce boilerplate de try/finally
# 4. Mejora legibilidad y seguridad
# 5. Compatible con archivos, locks, conexiones, sockets, etc.

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# - Usar with siempre que sea posible con recursos que requieren liberación
# - Implementar __enter__ y __exit__ en tus propias clases si manejan recursos
# - No capturar excepciones dentro de __exit__ a menos que sea necesario
# - Combinar with con logging para trazabilidad si ocurre error
