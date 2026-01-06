# casos_reales_context.md
=========================

Objetivo:
---------
Aprender cómo aplicar context managers en situaciones reales de desarrollo:
- Archivos
- Conexiones a bases de datos
- Locks y recursos compartidos
Todo con seguridad, limpieza automática y robustez.

---

## 1️⃣ ARCHIVOS

### Problema común
Abrir y cerrar archivos manualmente con `try/finally` es propenso a errores:

```python
# ❌ Mala práctica
f = open("datos.txt", "r")
try:
    contenido = f.read()
finally:
    f.close()

Solución con context manager

# ✅ Uso profesional
with open("datos.txt", "r") as f:
    contenido = f.read()

Ventajas:

    Archivo siempre se cierra aunque ocurra excepción

    Código limpio y legible

    Facilita debugging y mantenimiento

2️⃣ BASES DE DATOS
Context manager para conexión

from contextlib import contextmanager

@contextmanager
def conexion_db():
    db = conectar_db()  # función que inicializa conexión
    try:
        yield db
    finally:
        db.cerrar()  # siempre se cierra la conexión

Uso profesional

with conexion_db() as db:
    db.ejecutar_query("SELECT * FROM usuarios")

Ventajas:

    Evita fugas de conexiones

    Permite fail-fast si la conexión falla

    Código uniforme y mantenible

3️⃣ LOCKS Y RECURSOS COMPARTIDOS
Problema común

Bloqueos manuales pueden provocar deadlocks si olvidamos liberar el lock:

# ❌ Mala práctica
lock.acquire()
try:
    procesar_datos()
finally:
    lock.release()

Solución con context manager

import threading

lock = threading.Lock()

with lock:
    procesar_datos()

Ventajas:

    Bloqueo y desbloqueo automático

    Evita errores humanos

    Limpieza garantizada incluso si ocurre excepción

4️⃣ COMBINANDO CONTEXT MANAGERS

Se pueden anidar context managers para manejar múltiples recursos:

with open("datos.txt", "r") as f, conexion_db() as db, lock:
    contenido = f.read()
    db.ejecutar_query("INSERT INTO logs VALUES (?)", (contenido,))
    procesar_datos()

Ventajas:

    Múltiples recursos gestionados automáticamente

    Código compacto y seguro

    Facilita mantenimiento y debugging

5️⃣ BUENAS PRÁCTICAS PROFESIONALES

    Usar with siempre que sea posible para cualquier recurso que requiera limpieza.

    No capturar excepciones dentro de exit salvo que sea necesario, dejar que se propaguen.

    Incluir logging dentro de context managers para trazabilidad.

    Evitar anidamiento excesivo; si es complejo, dividir en funciones con sus propios context managers.

    Fail-fast: detectar errores de inicialización o liberación inmediatamente.

6️⃣ RESUMEN

    Context managers son la forma estándar y profesional de manejar recursos en Python.

    Archivos, DB, locks y sesiones se benefician de limpieza automática.

    Evitan errores comunes como fugas de recursos, deadlocks y datos inconsistentes.

    Su uso adecuado aumenta la robustez, mantenibilidad y claridad del código.