# Rate Limiting: Protegiendo tus Procesos y a Terceros

Lanzar miles de tareas asíncronas es fácil, pero tu servidor o la API que estás consultando tiene límites. El **Rate Limiting** (Limitación de Tasa) es el arte de controlar la velocidad de ejecución para no ser bloqueado o saturar recursos.

## 1. ¿Por qué es necesario?
- **Evitar 429 Too Many Requests:** Muchas APIs modernas te bloquearán la IP si haces más de N peticiones por segundo.
- **Protección de la Base de Datos:** Evitar que un proceso de fondo consuma todo el ancho de banda del disco o la conexión de red.
- **Ahorro de Costes:** Si pagas por uso de una API (como OpenAI), un error en un bucle async puede costarte miles de dólares en minutos si no tienes un límite de velocidad.

## 2. Estrategia: "Leaky Bucket" (Cubo con Goteo)
Es el algoritmo más común. Los trabajos entran a un cubo y salen por un agujero a una velocidad constante.
```python
async def rate_limited_worker(cola):
    while True:
        item = await cola.get()
        # Solo procesamos un ítem cada 0.1 segundos (máximo 10 por segundo)
        await asyncio.sleep(0.1) 
        await procesar(item)
        cola.task_done()
```

## 3. El Token Bucket
Permite breves picos de tráfico pero mantiene una media constante. Muy útil para aplicaciones web que tienen ráfagas de usuarios.

## 4. Implementación con Semáforos vs Sleep
- **Semáforo:** Limita cuántas cosas ocurren **al mismo tiempo** (concurrencia).
- **Sleep / Token Bucket:** Limita cuántas cosas ocurren **por unidad de tiempo** (tasa).
- **Senior Tip:** Muchas veces necesitarás ambos. Ej: "Máximo 5 conexiones simultáneas y máximo 50 peticiones por minuto".

## 5. Rate Limit Distribuido
Si tienes 10 servidores backend corriendo el mismo proceso, cada uno no puede tener su propio límite local.
- **Solución:** Los 10 servidores consultan un contador central en **Redis**. Redis ofrece operaciones atómicas rápidas para gestionar estos límites globales.

## Resumen: Cortesía Técnica
Tener un sistema que soporta 10.000 peticiones por segundo no significa que debas hacerlas. Un desarrollador senior diseña sus sistemas para que sean "buenos ciudadanos" de la red, respetando los límites propios y ajenos para garantizar la estabilidad a largo plazo.
