"""
EJERCICIOS: PIPELINES Y CONCURRENCIA REAL
-----------------------------------------------------------------------------
Retos basados en casos de negocio reales para poner a prueba tus habilidades.
"""

# EJERCICIO 1: EL SCRAPER RESILIENTE
# Crea un script que descargue el contenido de 50 URLs usando aiohttp.
# Requerimientos: 
# - Máximo 5 descargas simultáneas (Semáforo).
# - Si una URL falla, debe reintentarse hasta 3 veces con Exponential Backoff.

# EJERCICIO 2: PROCESADOR DE IMÁGENES EN PARALELO
# Tienes una carpeta con 100 imágenes (simuladas).
# Requerimientos:
# - Usa un Pool de procesos (Multiprocessing) para redimensionarlas.
# - Compara el tiempo que tarda con 1 proceso frente a 4 procesos.

# EJERCICIO 3: LA COLA DE PRIORIDAD DE PAGOS
# Implementa un sistema Productor-Consumidor con asyncio.PriorityQueue.
# - Los usuarios 'VIP' deben procesarse antes que los usuarios 'Standard'.
# - Simula que el procesamiento de cada pago tarda entre 1 y 2 segundos.

# EJERCICIO 4: FASTAPI BACKGROUND TASKS
# Crea un endpoint que reciba una petición, devuelva un ID de seguimiento 
# al instante, y lance una tarea de fondo que escriba ese ID en un archivo 
# tras 5 segundos de espera.

# EJERCICIO 5: DETECCIÓN DE BLOCKING IO
# Escribe una función 'async def' que intente hacer un cálculo pesado 
# y explica cómo usarías 'asyncio.to_thread()' para evitar que bloquee 
# el Event Loop de un servidor FastAPI.

"""
PROYECTO FINAL DEL TEMA:
------------------------
Construye una pequeña Pipeline ETL que:
1. Lea un archivo CSV de 10.000 filas (simulado).
2. Transforme los datos usando un Pool de procesos (Multiprocessing).
3. Envíe los resultados a una API mock asíncrona (Aiohttp) con un 
   límite de 20 peticiones por segundo.
4. Guarde en un archivo de logs 'fallas.txt' todos los registros que 
   no pudieron ser enviados tras 3 intentos.
"""
