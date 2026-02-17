# El Patrón Productor-Consumidor: La Base del Backend Escaldable

El patrón Productor-Consumidor es una de las arquitecturas más potentes de la computación. Permite separar **quién genera el trabajo** de **quién lo ejecuta**, eliminando cuellos de botella y permitiendo escalado asimétrico.

## 1. Los Actores
- **Productor:** Su única misión es detectar que algo debe hacerse (ej: un usuario sube una foto) y meter esa orden en una caja (Cola).
- **Cola (Broker):** Almacena los mensajes de forma ordenada y segura.
- **Consumidor (Worker):** Mira la caja, saca una orden y la ejecuta. Cuando termina, pide la siguiente.

## 2. Ventajas del Desacoplamiento
- **Suavizado de Picos (Smoothing):** Si tu servidor recibe 1.000 registros por segundo durante 1 minuto eñ mediodía, los productores los guardan en la cola y los consumidores los procesan a su ritmo durante los siguientes 10 minutos. Tu App no se cae por falta de CPU.
- **Escalado Independiente:** Si tienes mucho trabajo acumulado, solo tienes que levantar más "Workers" (Consumidores). No necesitas escalar tu servidor web principal.
- **Resiliencia:** Si un consumidor explota al procesar un dato, el dato sigue en la cola y otro consumidor puede intentarlo después.

## 3. Implementación Local vs Distribuida
- **Local (`asyncio.Queue`):** Ocurre dentro del mismo proceso Python. Veloz, pero si el proceso se cierra, la cola se vacía y los datos se pierden.
- **Distribuida (Redis/RabbitMQ):** La cola vive en un servidor aparte. Es persistente y permite que los consumidores estén en máquinas distintas a los productores.

## 4. El peligro de los Consumidores Lentos
Si el consumidor es mucho más lento que el productor y la cola es infinita, se producirá un agotamiento de memoria. Consulta la documentación de **Backpressure** en el Tema 07 para saber cómo gestionarlo.

## 5. Prioridades en la Cola
A veces, algunos trabajos son más importantes que otros (ej: procesar el pago de un cliente vs enviar un boletín de noticias). 
- **Solución Senior:** Usa `asyncio.PriorityQueue` para que los ítems con menor número de prioridad salgan antes de la cola.

## Resumen: Dividir para Vencer
Un desarrollador backend senior evita hacer tareas pesadas dentro del flujo de la petición HTTP. Usa el patrón Productor-Consumidor para responder rápido al cliente y delegar el trabajo duro a un sistema de colas robusto y monitorizado.
