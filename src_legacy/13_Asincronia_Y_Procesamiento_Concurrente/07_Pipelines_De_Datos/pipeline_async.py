"""
PIPELINES: ETL CONCURRENTE ASYNC
-----------------------------------------------------------------------------
Cómo diseñar una tubería de datos que procese información por etapas 
sin bloquearse. Utilizando asyncio.Queue para desacoplar procesos.
"""

import asyncio
import random

async def extractor(cola_entrada):
    """Paso 1: Obtiene datos (ej: de una API o DB)."""
    for i in range(1, 6):
        await asyncio.sleep(random.uniform(0.1, 0.5))
        datos = {"id": i, "valor": random.randint(1, 100)}
        print(f"[Extractor] Generado: {datos}")
        await cola_entrada.put(datos)
    
    # Señal de que ya no hay más datos
    await cola_entrada.put(None)

async def transformador(cola_entrada, cola_salida):
    """Paso 2: Limpia o modifica los datos."""
    while True:
        datos = await cola_entrada.get()
        if datos is None:
            await cola_salida.put(None)
            break
        
        # Simula transformación pesada
        await asyncio.sleep(0.3)
        datos["valor_final"] = datos["valor"] * 1.21 # Aplicar IVA
        print(f"  [Transformador] Procesado ID {datos['id']}")
        await cola_salida.put(datos)

async def cargador(cola_salida):
    """Paso 3: Guarda el resultado final (ej: en una DB)."""
    while True:
        datos = await cola_salida.get()
        if datos is None:
            break
        await asyncio.sleep(0.2)
        print(f"    [Cargador] GUARDADO FINAL: {datos}")

async def main():
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()

    print("[Main] Iniciando Pipeline...")
    # Ejecutamos todas las etapas a la vez
    await asyncio.gather(
        extractor(q1),
        transformador(q1, q2),
        cargador(q2)
    )
    print("[Main] Pipeline finalizada con éxito.")

if __name__ == "__main__":
    asyncio.run(main())

"""
VENTAJAS DE ESTE DISEÑO:
------------------------
1. Desacoplamiento: Cada etapa solo conoce su cola de entrada y salida.
2. Escalabilidad: Podrías lanzar 5 transformadores para procesar más 
   rápido si el extractor es muy veloz.
3. Eficiencia: Mientras el cargador espera a la DB, el transformador 
   puede seguir preparando el siguiente dato.
"""
