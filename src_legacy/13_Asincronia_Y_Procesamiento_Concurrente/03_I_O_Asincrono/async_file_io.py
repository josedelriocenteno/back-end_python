"""
ASYNC I/O: ARCHIVOS CON AIOFILES
-----------------------------------------------------------------------------
Aunque parezca mentira, Python estándar NO tiene soporte nativo para 
E/S de archivos asíncrona (el SO los maneja de forma bloqueante). 
Usamos 'aiofiles' para evitar detener el Event Loop.
"""

import asyncio
import aiofiles
import os

async def escribir_log_async(filename, contenido):
    """Escribe en un archivo de forma asíncrona."""
    # 'async with' asegura que el puntero se libera correctamente
    async with aiofiles.open(filename, mode='a') as f:
        await f.write(f"{contenido}\n")
    print(f"✅ Línea escrita en {filename}")

async def leer_archivo_async(filename):
    """Lee un archivo línea a línea sin bloquear."""
    async with aiofiles.open(filename, mode='r') as f:
        async for line in f:
            # Procesamos cada línea...
            print(f"  [Read] {line.strip()}")

async def main():
    fname = "temp_async.txt"
    
    # 1. Escribimos varias líneas concurrentemente
    await asyncio.gather(
        escribir_log_async(fname, "Log evento A"),
        escribir_log_async(fname, "Log evento B"),
        escribir_log_async(fname, "Log evento C")
    )

    # 2. Leemos el resultado
    await leer_archivo_async(fname)
    
    # Limpieza
    if os.path.exists(fname): os.remove(fname)

if __name__ == "__main__":
    asyncio.run(main())

"""
LA REALIDAD TECNICA:
--------------------
La mayoría de los SO actuales no ofrecen una API asíncrona para archivos 
de disco tan fluida como la de red (sockets). 'aiofiles' soluciona esto 
ejecutando las operaciones pesadas de archivo en un Pool de hilos 
separado, para que tu Event Loop principal nunca se detenga.
"""

"""
USO RECOMENDADO:
----------------
Usa asincronía para archivos si tu App maneja muchos archivos pequeños 
o si estás leyendo/escribiendo logs constantemente bajo mucha carga. 
Si solo lees un archivo de configuración al arrancar, la versión síncrona 
estándar ('open()') es suficiente.
"""
