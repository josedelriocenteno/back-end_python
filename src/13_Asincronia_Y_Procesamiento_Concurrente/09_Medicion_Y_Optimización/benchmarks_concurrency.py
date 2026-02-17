"""
BENCHMARKS: COMPARATIVA DE RENDIMIENTO
-----------------------------------------------------------------------------
Script para medir la diferencia de velocidad real entre 
Síncrono vs Threading vs Asyncio.
"""

import time
import asyncio
import threading
import requests
import httpx

URL = "https://www.google.com"
N_PETICIONES = 10

def sync_run():
    start = time.perf_counter()
    for _ in range(N_PETICIONES):
        requests.get(URL)
    return time.perf_counter() - start

def thread_run():
    start = time.perf_counter()
    threads = []
    for _ in range(N_PETICIONES):
        t = threading.Thread(target=requests.get, args=(URL,))
        threads.append(t)
        t.start()
    for t in threads: t.join()
    return time.perf_counter() - start

async def async_run():
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        tasks = [client.get(URL) for _ in range(N_PETICIONES)]
        await asyncio.gather(*tasks)
    return time.perf_counter() - start

if __name__ == "__main__":
    print(f"--- Benchmark: {N_PETICIONES} peticiones a {URL} ---")
    
    t_sync = sync_run()
    print(f"Síncrono: {t_sync:.2f}s")
    
    t_thread = thread_run()
    print(f"Threading: {t_thread:.2f}s")
    
    t_async = asyncio.run(async_run())
    print(f"Asyncio:   {t_async:.2f}s")

"""
CONCLUSIONES DEL BENCHMARK:
---------------------------
1. Síncrono es el más lento (N * tiempo_latencia).
2. Threading y Asyncio deberían tardar casi lo mismo (~tiempo_latencia_máxima).
3. A medida que N sube a 1.000, Threading fallará o consumirá demasiada 
   RAM del sistema, mientras que Asyncio seguirá funcionando de forma ligera.
"""
