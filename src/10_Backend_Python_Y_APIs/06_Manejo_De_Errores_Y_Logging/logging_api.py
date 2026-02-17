"""
LOGGING PROFESIONAL EN APIs
-----------------------------------------------------------------------------
Los logs son los ojos del desarrollador en producción. Un log vacío es un 
backend ciego.
"""

import logging
import sys

# 1. CONFIGURACIÓN DEL LOGGER
# Usamos un logger específico para nuestra app, no el de root.
logger = logging.getLogger("my_api")
logger.setLevel(logging.INFO)

# Formateador: Fecha - Nombre - Nivel - Mensaje
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

# Salida a terminal (stdout)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/process")
async def process_something(user_id: str):
    # TIP DE NIVEL: Usa logs estructurados
    logger.info(f"Iniciando proceso pesado para el usuario: {user_id}")
    
    try:
        # Lógica...
        result = 10 / 1 # Simulamos éxito
        logger.info(f"Proceso completado con éxito para: {user_id}")
        return {"result": result}
    except Exception as e:
        # El nivel ERROR dispara alertas; añade la traza completa (exc_info)
        logger.error(f"Fallo crítico en proceso para usuario {user_id}", exc_info=True)
        return {"error": "Internal fall"}

"""
RESUMEN DE NIVELES DE LOG:
1. DEBUG: Información muy detallada (ej: la query SQL exacta). Desactivado en prod.
2. INFO: Eventos normales (ej: 'Servidor iniciado', 'Login exitoso').
3. WARNING: Algo raro pasó pero no rompió la app (ej: 'Reintento de conexión').
4. ERROR: Algo falló en un request (ej: 'Fallo al guardar en DB').
5. CRITICAL: El sistema entero está en peligro (ej: 'Sin espacio en disco').
"""

"""
LOGS ESTRUCTURADOS:
Si usas herramientas como ELK o CloudWatch, considera usar un formateador 
de JSON para que tus logs se puedan filtrar por campos como 'user_id' o 'endpoint'.
"""
