# Pipelines Streaming: Datos en Tiempo Real

El procesamiento por streaming (o "real-time") se encarga de procesar cada dato en el momento exacto en que se genera.

## 1. Funcionamiento del Streaming
Los datos se tratan como un flujo infinito. En lugar de procesar "archivos", procesas "eventos" individuales (un click, una compra, un log de error).

## 2. Ventajas del Streaming
- **Baja Latencia:** Reacción inmediata ante eventos (ej: detectar un fraude bancario en el segundo que ocurre).
- **Flujo Constante:** No saturas el sistema con picos de trabajo gigantes (como pasa en el batch); la carga se distribuye a lo largo del día.

## 3. Desventajas: Complejidad Extrema
- **Out-of-order data:** ¿Qué pasa si el evento 1 llega después del evento 2 porque la red falló?
- **Estado Dinámico:** Es difícil hacer sumas (agregaciones) cuando los datos nunca terminan de llegar.
- **Coste:** Mantener servidores escuchando 24/7 suele ser más caro que encender una máquina 10 minutos al día para el batch.

## 4. Herramientas Estándar
- **Apache Kafka:** La columna vertebral (cola de eventos).
- **Apache Flink / Spark Streaming:** El cerebro que procesa los eventos.
- **AWS Kinesis / Google PubSub:** Servicios gestionados de nube.

## 5. Caso de Uso: Detección de Fraude
Si una tarjeta se usa en Madrid y 1 minuto después en Tokio, necesitas una alerta inmediata para bloquear la transacción. El batch de mañana sería demasiado tarde.

## Resumen: Velocidad y Reacción
El streaming es para cuando el tiempo es dinero. Requiere una arquitectura mucho más sofisticada (Kafka, microservicios) pero permite que la empresa sea proactiva en lugar de reactiva.
