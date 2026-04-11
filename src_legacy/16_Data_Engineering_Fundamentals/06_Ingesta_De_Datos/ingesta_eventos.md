# Ingesta de Eventos: Streaming y Mensajería

A diferencia del batch (donde vas a buscar el dato), en la ingesta de eventos el dato "te llega" en el momento en que ocurre (Push).

## 1. El Broker de Mensajes
Necesitas un intermediario que reciba los eventos y los guarde temporalmente hasta que tu pipeline los procese.
- **Kafka:** El estándar para alto volumen y persistencia (guarda los mensajes en disco).
- **RabbitMQ:** Excelente para enrutamiento complejo pero suele borrar el mensaje tras ser leído.

## 2. El Productor y el Consumidor
- **Producer:** La App de Backend que envía el evento `user_logged_in`.
- **Consumer:** Tu pipeline de datos que escucha ese evento y lo guarda en el Data Lake.

## 3. Ventajas de la Arquitectura de Eventos
- **Desacoplamiento:** La App de Backend no tiene que saber nada de tu base de datos. Solo envía un mensaje al aire.
- **Escalabilidad:** Puedes tener 10 consumidores leyendo de la misma cola para repartirse el trabajo si hay un pico de tráfico.

## 4. Change Data Capture (CDC)
Es la forma más avanzada de ingesta de eventos. En lugar de que el desarrollador de Backend envíe un evento manual, usamos una herramienta (como **Debezium**) que escucha el log de la base de datos (WAL en Postgres). 
- Cada vez que alguien hace un `INSERT` en la DB, Debezium lo convierte en un evento de Kafka automáticamente.

## 5. El reto: "Exactly Once Ingestion"
Asegurar que un evento no se ingiere dos veces si el consumidor se reinicia. Requiere que el consumidor guarde el **Offset** (la posición del mensaje en la cola) de forma atómica con la escritura en la base de datos.

## Resumen: Reactividad Total
La ingesta de eventos es la base de la empresa en tiempo real. Permite que los datos fluyan de forma continua y que la analítica sea un reflejo vivo de lo que está pasando en el producto en cada segundo.
