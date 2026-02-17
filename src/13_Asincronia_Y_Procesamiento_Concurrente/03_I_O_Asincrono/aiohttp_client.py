"""
ASYNC I/O: HTTP CON AIOHTTP
-----------------------------------------------------------------------------
Cómo realizar cientos de peticiones HTTP en paralelo de forma eficiente.
"""

import asyncio
import aiohttp
import time

async def fetch_url(session, url):
    """Realiza una petición GET de forma asíncrona."""
    async with session.get(url) as response:
        # Importante: el .text() o .json() también son 'await' porque 
        # requieren leer el cuerpo de la red.
        status = response.status
        data = await response.text()
        return f"URL {url} -> {status} (size: {len(data)})"

async def main():
    urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://www.github.com",
        "https://api.github.com/events"
    ]

    start = time.perf_counter()

    # 1. CLIENTSESSION: Es vital reusar la sesión para aprovechar 
    # las conexiones TCP abiertas (Connection Pooling).
    async with aiohttp.ClientSession() as session:
        # Creamos una lista de corrutinas
        tasks = [fetch_url(session, url) for url in urls]
        
        # Ejecutamos todas en paralelo
        resultados = await asyncio.gather(*tasks)
        
        for r in resultados:
            print(r)

    end = time.perf_counter()
    print(f"\n[AIOHTTP] Total tiempo: {end - start:.2f} segundos")

if __name__ == "__main__":
    asyncio.run(main())

"""
¿POR QUÉ NO USAR REQUESTS?
--------------------------
Librerías como 'requests' son síncronas. Si las metes en un bucle async, 
cada petición esperará a que termine la anterior antes de empezar la 
siguiente. Con 'aiohttp' o 'httpx', todas las peticiones salen a la red 
al mismo tiempo.
"""

"""
REGLA DE ORO DE SESIONES:
-------------------------
NUNCA crees una sesión nueva para cada petición. 'aiohttp.ClientSession' 
está diseñada para vivir durante todo el ciclo de vida de tu App (o al 
menos durante el lote de peticiones) para ser realmente eficiente.
"""
