# ¿Qué son las Trazas (Tracing)?

Las **Trazas** son el tercer pilar de la observabilidad. Representan el seguimiento de una solicitud (request) individual a medida que se desplaza a través de los diversos componentes de un sistema distribuido.

## 1. El concepto de "Span"
Una traza se compone de múltiples **Spans**.
*   **Trace (Traza):** Es el viaje completo del usuario (ej: de principio a fin de una compra).
*   **Span:** Una unidad de trabajo individual dentro de la traza (ej: "Llamada a la DB de inventario", "Validación del pago", "Envío de email"). Cada span tiene un nombre, un tiempo de inicio y un tiempo de fin.

## 2. El árbol de la petición
Las trazas se visualizan como una cascada o un árbol:
- Span 1: API Request (1.2s)
  - Span 2: Auth Check (100ms)
  - Span 3: DB Query (800ms)
  - Span 4: Cache Update (50ms)
Esto permite ver instantáneamente que el **80% del tiempo se perdió en la base de datos**.

## 3. Contexto distribuido (Context Propagation)
¿Cómo sabe el microservicio de "Inventario" que pertenece a la misma traza que el microservicio de "Pedidos"?
*   Usando **Trace IDs**. 
*   El primer servicio crea un ID (ej: `trace-123`) y lo envía en las cabeceras HTTP (`X-Trace-Id`) a todos los servicios que llama.

## 4. ¿Por qué es vital para el Data Engineer?
En pipelines complejos:
*   Un dato pasa por: Ingesta -> S3 -> Spark -> Redshift -> BI.
*   Si el dato final es erróneo, la trazabilidad nos permite saber exactamente en qué paso de la cadena se corrompió.

## 5. El estándar: OpenTelemetry (OTel)
OpenTelemetry es el estándar de la industria que permite recoger trazas, métricas y logs de forma unificada sin quedar atrapado con un solo proveedor (vendor lock-in).

## Resumen: Siguiendo el rastro
Las trazas te dan la vista de pájaro de cómo interactúan tus servicios. Permiten identificar cuellos de botella y errores silenciosos en sistemas distribuidos que serían imposibles de encontrar mirando solo logs individuales.
