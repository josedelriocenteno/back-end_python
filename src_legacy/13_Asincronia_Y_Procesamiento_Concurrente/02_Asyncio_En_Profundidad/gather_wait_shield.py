"""
ASYNCIO: COORDINACIÓN (GATHER, WAIT, SHIELD)
-----------------------------------------------------------------------------
Diferentes formas de esperar a que múltiples cosas terminen.
"""

import asyncio

async def worker(t, exit_mode="ok"):
    await asyncio.sleep(t)
    if exit_mode == "error":
        raise ValueError(f"Fallo en worker {t}")
    return f"Worker {t} ok"

async def main():
    print("--- 1. GATHER (Todo o nada) ---")
    # gather() es ideal si necesitas todos los resultados para seguir.
    # Si uno falla, gather lanzará la excepción, pero las otras tareas 
    # seguirán corriendo de fondo (¡cuidado!).
    try:
        resultados = await asyncio.gather(worker(1), worker(2, "error"))
    except ValueError as e:
        print(f"Error detectado: {e}")

    print("\n--- 2. WAIT (Control granular) ---")
    # wait() devuelve dos conjuntos: terminadas y pendientes.
    # Puedes decir que vuelva en cuanto termine la PRIMERA (FIRST_COMPLETED)
    done, pending = await asyncio.wait(
        [worker(1), worker(3)],
        return_when=asyncio.FIRST_COMPLETED
    )
    print(f"Terminadas: {len(done)}, Pendientes: {len(pending)}")
    for p in pending: p.cancel() # Limpieza manual obligatoria

    print("\n--- 3. SHIELD (El escudo) ---")
    # shield() protege a una corrutina de ser cancelada desde fuera.
    # Útil para tareas críticas que NO deben interrumpirse (ej: guardar en DB)
    tarea_critica = asyncio.create_task(worker(1))
    protected = asyncio.shield(tarea_critica)
    # Si alguien cancela 'protected', 'tarea_critica' seguirá viva.

if __name__ == "__main__":
    asyncio.run(main())

"""
¿CUÁNDO USAR QUÉ?
-----------------
- GATHER: Cuando quieres sencillez y necesitas todos los valores.
- WAIT: Cuando necesitas rapidez (ej: llamar a 3 servidores y usar el 
  que responda antes).
- SHIELD: Cuando la operación es atómica y no puede dejarse a medias.
"""
