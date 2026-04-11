"""
PYTEST: TESTING ASÍNCRONO CON PYTEST-ASYNCIO
-----------------------------------------------------------------------------
Cómo testear funciones 'async def' y gestionar el bucle de eventos (Event Loop).
"""

import pytest
import asyncio

# 1. LA FUNCIÓN ASÍNCRONA
async def suma_asincrona(a, b):
    await asyncio.sleep(0.01) # Simula una operación de E/S
    return a + b

# 2. CONFIGURACIÓN DEL TEST ASÍNCRONO
# Por defecto, pytest no entiende 'async def'. 
# Necesitamos el decorador '@pytest.mark.asyncio'
@pytest.mark.asyncio
async def test_suma_asincrona():
    resultado = await suma_asincrona(5, 10)
    assert resultado == 15

# 3. FIXTURES ASÍNCRONAS
@pytest.fixture
async def conexion_async_db():
    print("\n[SETUP] Abriendo conexión async...")
    conn = {"status": "connected"}
    yield conn
    print("\n[TEARDOWN] Cerrando conexión async...")

@pytest.mark.asyncio
async def test_uso_de_conexion_async(conexion_async_db):
    assert conexion_async_db["status"] == "connected"

"""
¿POR QUÉ ES DIFERENTE EL TESTING ASÍNCRONO?
-------------------------------------------
1. Event Loop: Los tests deben correr dentro de un bucle de eventos. 
   Pytest-asyncio se encarga de crearlo y cerrarlo por ti.
2. Await: Si olvidas el 'await' en un test, el test pasará (verde) pero 
   en realidad no habrás ejecutado nada. Es un falso positivo muy común.
3. Velocidad: Los tests asíncronos permiten ejecutar múltiples tareas de 
   E/S en paralelo, lo que puede acelerar mucho la suite de tests si tienes 
   muchas llamadas a mock APIs o DBs.
"""

"""
CONSEJO SENIOR:
---------------
Crea un archivo 'pytest.ini' y añade:
[pytest]
asyncio_mode = auto
Esto hará que TODOS los 'async def test_...' funcionen sin necesidad 
de poner el decorador @pytest.mark.asyncio en cada uno.
"""
