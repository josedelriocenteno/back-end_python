"""
contextlib_usage.py
==================

Objetivo:
- Crear context managers de manera simple con contextlib.contextmanager
- Reducir boilerplate de clases
- Mantener control profesional de recursos
"""

# -------------------------------------------------------------------
# 1️⃣ IMPORTAR EL DECORADOR
# -------------------------------------------------------------------

from contextlib import contextmanager

# -------------------------------------------------------------------
# 2️⃣ CREAR UN CONTEXT MANAGER SIMPLE
# -------------------------------------------------------------------

@contextmanager
def abrir_archivo(path: str, modo: str):
    """Context manager para abrir archivos"""
    f = open(path, modo)
    try:
        print(f"Abriendo archivo {path}")
        yield f  # lo que se devuelve al bloque 'with'
    finally:
        f.close()
        print(f"Cerrando archivo {path}")

# -------------------------------------------------------------------
# 3️⃣ USO DEL CONTEXT MANAGER
# -------------------------------------------------------------------

with abrir_archivo("datos.txt", "w") as f:
    f.write("Hola mundo\n")
    print("Escribiendo en el archivo...")

# Output:
# Abriendo archivo datos.txt
# Escribiendo en el archivo...
# Cerrando archivo datos.txt

# Ventaja:
# - Código más compacto
# - Limpieza automática del recurso
# - Manejo seguro incluso si ocurre excepción

# -------------------------------------------------------------------
# 4️⃣ CONTEXT MANAGER CON EXCEPCIONES
# -------------------------------------------------------------------

@contextmanager
def conexion_db_simulada():
    """Simula una conexión a base de datos"""
    print("Conexión abierta")
    try:
        yield "conexión"
    except Exception as e:
        print(f"Ocurrió excepción en DB: {e}")
        raise  # Propaga la excepción
    finally:
        print("Conexión cerrada")

# Uso
try:
    with conexion_db_simulada() as db:
        print("Ejecutando query")
        # raise RuntimeError("Error de prueba")  # probar manejo
except RuntimeError as e:
    print(f"Excepción capturada fuera del with: {e}")

# Output si hay excepción:
# Conexión abierta
# Ejecutando query
# Ocurrió excepción en DB: Error de prueba
# Conexión cerrada
# Excepción capturada fuera del with: Error de prueba

# -------------------------------------------------------------------
# 5️⃣ VENTAJAS DEL DECORADOR contextmanager
# -------------------------------------------------------------------

# 1. Código más compacto y legible
# 2. No requiere definir clase completa
# 3. yield → divide setup y cleanup
# 4. Manejo automático de excepciones con finally
# 5. Ideal para archivos, conexiones, locks, sesiones, etc.

# -------------------------------------------------------------------
# 6️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# - Siempre usar try/finally dentro del context manager para cleanup
# - Yield solo una vez por contexto
# - Propaga excepciones fuera del with si no se pueden manejar localmente
# - Combinar logging con context manager para trazabilidad
