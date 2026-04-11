"""
FASTAPI: EL PODER DE ASYNC DEF
-----------------------------------------------------------------------------
Cómo FastAPI aprovecha asyncio para dar un rendimiento de nivel elite.
"""

from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

# 1. ENDPOINT ASINCRÓNICO (Recomendado para I/O)
@app.get("/async-call")
async def get_external_data():
    """
    Este endpoint es eficiente. Mientras espera la API de GitHub, 
    FastAPI puede atender otros cientos de peticiones.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/")
        return {"data": response.json()}

# 2. ENDPOINT SÍNCRÓNICO (Normal)
@app.get("/sync-call")
def get_sync_data():
    """
    FastAPI es inteligente: si NO pones 'async def', ejecuta esta función 
    en un Pool de hilos externo para NO bloquear el Event Loop.
    """
    return {"message": "Ejecutado en un hilo aparte"}

# 3. EL GRAN PELIGRO: 'async def' + código bloqueante
@app.get("/vulnerable")
async def im_dangerous():
    """
    ¡¡MAL!! Al ser 'async def', FastAPI la corre en el Event Loop principal.
    Como hemos puesto un sleep síncrono, TODO EL SERVIDOR SE DETIENE. 
    Ningún otro usuario podrá entrar hasta que pasen 5 segundos.
    """
    import time
    time.sleep(5) 
    return {"status": "He roto el servidor por 5 segundos"}

"""
REGLA SENIOR:
-------------
- Si haces I/O (DB, API) -> Usa 'async def' y librerías async con await.
- Si no estás seguro o usas librerías viejas -> Usa 'def' normal. 
- NUNCA uses 'async def' con funciones que no tengan 'await' dentro 
  y que tarden mucho tiempo.
"""
