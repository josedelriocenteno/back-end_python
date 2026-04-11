# Apache Kafka: El sistema circulatorio del dato

Kafka no es una base de datos ni una simple cola de mensajes. Es una plataforma de "Event Streaming" distribuida capaz de manejar billones de eventos al día con bajísima latencia.

## 1. Arquitectura de Kafka
- **Topics (Tópicos):** Son las "tuberías" donde se publican los mensajes (ej: `logs_servidor` o `transacciones_bancarias`).
- **Producers:** El sistema que envía el dato (ej: la App Web).
- **Consumers:** El sistema que lee el dato (ej: tu pipeline de datos).
- **Brokers:** Los servidores que forman el clúster de Kafka y guardan los mensajes.

## 2. Persistencia y Rebobinado
A diferencia de otras colas, Kafka guarda los mensajes en disco durante un tiempo determinado (ej: 7 días). Si tu pipeline falla, puedes "rebobinar" y volver a leer los mensajes desde el principio de la semana.

## 3. Particionado en Kafka
Un tópico se divide en particiones. Esto permite que varios consumidores lean el mismo tópico en paralelo, cada uno encargándose de una partición diferente. Es la clave de su velocidad.

## 4. Kafka Connect
Es un ecosistema de conectores listos para usar. Permite mover datos de Postgres a Kafka o de Kafka a S3 sin escribir una sola línea de código, solo configurando un archivo JSON.

## 5. El ecosistema "Event-Driven"
Kafka permite que la empresa no sea una serie de bases de datos aisladas, sino un flujo continuo de eventos donde cada equipo puede "enchufarse" para leer lo que necesite en tiempo real.

## Resumen: La columna vertebral
Kafka es lo que permite que una empresa pase de "procesar archivos por la noche" a "reaccionar al mundo en el segundo en que ocurre". Es la pieza central de cualquier arquitectura de datos moderna y de alta disponibilidad.
