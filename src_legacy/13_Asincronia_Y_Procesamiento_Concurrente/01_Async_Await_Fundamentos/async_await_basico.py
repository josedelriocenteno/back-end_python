"""
ASYNCIO: SINTAXIS REAL Y CORRUTINAS
-----------------------------------------------------------------------------
Cómo definir y llamar a funciones asíncronas sin morir en el intento.
"""

import asyncio

# 1. DEFINICIÓN: 'async def' crea un objeto Corrutina, NO ejecuta el código.
async def saludar():
    return "Hola desde el futuro"

# 2. LLAMADA INCORRECTA
def error_comun():
    # Esto NO imprime el saludo, imprime un objeto <coroutine object...>
    # Además, Python lanzará un RuntimeWarning avisando que nunca se ejecutó.
    obj = saludar()
    print(f"Error: {obj}")

# 3. LLAMADA CORRECTA: 'await'
async def forma_correcta():
    # 'await' solo se puede usar dentro de otra función 'async'
    mensaje = await saludar()
    print(f"Correcto: {mensaje}")

# 4. EJECUCIÓN DESDE EL MUNDO SÍNCRONO (Entry Point)
if __name__ == "__main__":
    # error_comun() 
    asyncio.run(forma_correcta())

"""
LA CADENA DE AWAIT:
-------------------
Para que la asincronía funcione, debe haber una "cadena de mando" desde 
el asyncio.run() hasta la última función de E/S. Si en medio de la 
cadena llamas a una función async de forma síncrona (olvidando el await), 
rompes el flujo y el código no se ejecutará como esperas.
"""

"""
¿QUÉ ES UNA CORRUTINA? (Concepto Senior)
----------------------------------------
Es una función que puede pausar su ejecución y reanudarla más tarde 
manteniendo su estado interno (variables locales). A nivel interno de 
Python, las corrutinas son una evolución de los Generadores (`yield`).
"""
