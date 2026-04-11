"""
finally_usage.py
================

Objetivo:
- Entender cómo usar `finally` para limpiar recursos
- Garantizar consistencia y evitar fugas (archivos, conexiones, locks)
- Separar lógica de negocio del manejo de recursos
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO BÁSICO: ARCHIVOS
# -------------------------------------------------------------------

# ❌ Mala práctica: abrir archivo sin finally
try:
    f = open("datos.txt", "r")
    contenido = f.read()
    print(contenido)
except FileNotFoundError as e:
    print(f"Error: {e}")
# Si ocurre otro error, archivo queda abierto ❌

# ✅ Buena práctica: usar finally para cerrar
f = None
try:
    f = open("datos.txt", "r")
    contenido = f.read()
    print(contenido)
except FileNotFoundError as e:
    print(f"Error: {e}")
finally:
    if f:
        f.close()
        print("Archivo cerrado de forma segura ✅")

# -------------------------------------------------------------------
# 2️⃣ EJEMPLO CON CONEXIONES (simulado)
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

    def ejecutar(self, query):
        if not self.abierta:
            raise RuntimeError("Conexión cerrada")
        print(f"Ejecutando query: {query}")

# Uso correcto con finally
db = ConexionDB()
try:
    db.abrir()
    db.ejecutar("SELECT * FROM usuarios")
except RuntimeError as e:
    print(f"Error en DB: {e}")
finally:
    if db.abierta:
        db.cerrar()
        print("Conexión cerrada en finally ✅")

# -------------------------------------------------------------------
# 3️⃣ EJEMPLO CON LOCKS
# -------------------------------------------------------------------

import threading

lock = threading.Lock()

# ❌ Mala práctica: no liberar lock si ocurre error
try:
    lock.acquire()
    # código crítico que puede fallar
    x = 1 / 0  # RuntimeError
finally:
    lock.release()  # ✅ Siempre se ejecuta, previene deadlocks

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS CON FINALLY
# -------------------------------------------------------------------

# 1. Usar finally para liberar cualquier recurso externo (archivos, DB, locks)
# 2. Separar lógica de negocio de manejo de recursos
# 3. Nunca depender de except para liberar recursos
# 4. Para archivos y otros objetos con contexto, usar `with` (context managers)
#    es preferible a try/finally manual
# 5. Asegurar que el código en finally **no lance excepciones** inesperadas
