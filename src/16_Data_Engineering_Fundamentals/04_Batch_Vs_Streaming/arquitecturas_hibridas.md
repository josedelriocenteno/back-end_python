# Arquitecturas Híbridas: Lambda vs. Kappa

¿Y si queremos lo mejor de ambos mundos? (La robustez del batch y la velocidad del streaming). Aquí entran las arquitecturas de referencia.

## 1. Arquitectura Lambda
Es la más clásica. Divide el sistema en dos capas:
- **Speed Layer (Streaming):** Procesa datos recientes rápidamente pero con margen de error o sin toda la historia.
- **Batch Layer (Master Dataset):** Procesa todos los datos del pasado con máxima precisión.
- **Serving Layer:** Junta ambos resultados para el usuario.
- **Contra:** Tienes que escribir y mantener el código de transformación **dos veces** (una en streaming y otra en batch).

## 2. Arquitectura Kappa
Es la evolución impulsada por los creadores de Kafka.
- **Idea:** Todo es streaming. El historial (los datos pasados) se guardan en el mismo sistema de eventos (Kafka) con una retención muy larga.
- **Pro:** Solo mantienes **un código**. Si quieres re-procesar los últimos 2 años, simplemente "rebobinas" el flujo de eventos y lo vuelves a pasar por el procesador.

## 3. Unified Batch and Streaming (Apache Beam)
Plataformas como Google Cloud Dataflow o Apache Beam permiten escribir un código que funciona igual en batch que en streaming. Tú solo cambias la fuente (un archivo o una cola).

## 4. Cuál elegir hoy
- **Lambda:** Si tienes sistemas legacy que no puedes cambiar y necesitas añadir una capa rápida encima.
- **Kappa:** Si empiezas un proyecto desde cero y quieres sencillez de mantenimiento a largo plazo.

## Resumen: Convergencia
La tendencia actual es que la barrera entre batch y streaming desaparezca. Los sistemas modernos tienden a tratar el batch como un "caso especial de streaming con fin", permitiendo arquitecturas más limpias y fáciles de operar.
