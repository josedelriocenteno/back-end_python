# Streaming Processing: La cultura del evento

El streaming no es solo "batch rápido". Es un cambio de paradigma: el dato se procesa a medida que fluye, sin principio ni fin.

## 1. El concepto de Ventana (Windowing)
Como el flujo es infinito, para hacer cálculos (ej: media de ventas) necesitamos "cortar" el flujo en trozos temporales:
- **Tumbling Windows:** Ventanas fixas que no se solapan (ej: cada 5 min exactos).
- **Sliding Windows:** Ventanas que se solapan (ej: la media de los últimos 5 min, calculada cada minuto).
- **Session Windows:** Se basan en la actividad del usuario (ej: desde que el usuario entra hasta que pasan 30 min de inactividad).

## 2. Tiempo de Evento vs. Tiempo de Procesamiento
- **Event Time:** Cuándo ocurrió el evento realmente en el mundo real.
- **Processing Time:** Cuándo llegó el evento a nuestro servidor.
- **Tip Senior:** Usa siempre **Event Time**. Si un móvil se queda sin cobertura y envía los datos 1 hora tarde, tu pipeline debe ser capaz de "viajar al pasado" y colocar ese dato en la hora correcta.

## 3. Watermarks (Marcas de agua)
Son el mecanismo para manejar datos que llegan tarde. Un Watermark dice: "No espero más datos de antes de las 10:00; a partir de ahora, cualquier dato que llegue con hora 09:59 será ignorado o tratado como excepción".

## 4. Semántica de Entrega
- **At Most Once:** El dato puede perderse, pero nunca se duplica.
- **At Least Once:** El dato llegará seguro, pero puede repetirse.
- **Exactly Once:** El santo grial. El sistema garantiza que cada evento se procesa una y solo una vez. Es difícil de lograr y requiere herramientas como Kafka + Flink.

## Resumen: Respuesta Inmediata
El streaming permite crear experiencias "vivas": notificaciones push instantáneas, ajustes de precios según la demanda en tiempo real y detección inmediata de errores críticos.
