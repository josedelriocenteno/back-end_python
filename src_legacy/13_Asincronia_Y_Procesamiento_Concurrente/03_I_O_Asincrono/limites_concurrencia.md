# Límites de Concurrencia: El Semáforo

Como hemos visto, el poder de `asyncio` es peligroso. Si lanzas 5.000 peticiones HTTP a una API externa a la vez, probablemente te bloqueen por sospecha de ataque DDoS. Necesitas poner un **Límite de Concurrencia**.

## 1. El Semáforo (`asyncio.Semaphore`)
Un semáforo es un contador que solo permite el paso de N tareas a la vez. Si el semáforo es de 10, y hay 100 tareas, las 90 restantes esperarán cola ordenadamente.

```python
sem = asyncio.Semaphore(10) # Máximo 10 a la vez

async def tarea_limitada(id):
    async with sem:
        # Aquí solo puede haber 10 personas a la vez
        await llamar_servicio_externo()
```

## 2. Por qué limitar es de "Senior"
- **Protección de la DB:** Evitas saturar el pool de conexiones.
- **Protección de la Red:** Evitas agotar el ancho de banda.
- **Cortesía con APIs de Terceros:** Respetas los límites de cuota (Rate Limits) para evitar bloqueos de IP.
- **Estabilidad de Memoria:** Cada tarea viva en `asyncio` consume un poco de RAM. Lanzar 1 millón de tareas de golpe puede agotar la memoria del servidor.

## 3. Backpressure (Presión de Retorno)
Si tu sistema recibe 1.000 mensajes por segundo pero solo puede procesar 100, la cola crecerá infinitamente. Poner límites de concurrencia te permite detectar este problema pronto y avisar al sistema emisor ("System Overloaded").

## 4. Semáforos vs Queues
- **Semaphore:** Útil para cuando ya tienes las tareas creadas y quieres controlar su paso.
- **Queue:** Útil para cuando tienes productores enviando datos y quieres que un número fijo de workers (ej: 5) los procesen de forma constante.

## 5. El error de "Un solo Semáforo para todo"
No uses un semáforo global. Crea semáforos específicos para cada recurso crítico. Un semáforo para la API de pagos y otro distinto para las llamadas a la base de datos.

## Resumen: Controlar la inundación
La asincronía es como una manguera de alta presión. Los semáforos son la válvula que te permite controlar el flujo para regar el jardín sin inundar la casa.
