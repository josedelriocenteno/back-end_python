# Diseño de Arquitecturas de Pipelines

Diseñar una tubería de datos profesional requiere pensar en la topología (forma) del flujo de datos. Dependiendo del problema, elegirás una estructura u otra.

## 1. Fan-Out / Fan-In
- **Fan-Out (Dispersión):** Un extractor envía datos a varios transformadores en paralelo para aumentar la velocidad.
- **Fan-In (Concentración):** Varios procesos terminan enviando sus resultados a un único cargador (ej: una única conexión a DB) para evitar bloqueos.

## 2. Micro-batching (Micro-lotes)
En lugar de procesar registro a registro, acumulas 100 registros y los procesas juntos.
- **Ventaja:** Mucho más eficiente para la base de datos (hacer un `INSERT` de 100 filas es 10 veces más rápido que hacer 100 `INSERT` de 1 fila).
- **Desventaja:** Añade latencia (el primer dato del lote tiene que esperar a que llegue el número 100).

## 3. Stateless vs Stateful (Con o sin estado)
- **Stateless:** Cada dato se procesa sin importar lo que pasó antes. Es fácil de escalar.
- **Stateful:** El procesamiento de un dato depende de los anteriores (ej: calcular la media móvil de las últimas 10 ventas). Requiere memoria compartida o una DB intermedia (Redis).

## 4. Push vs Pull
- **Push:** El productor empuja el dato al siguiente paso en cuanto lo tiene. Es más rápido (baja latencia).
- **Pull:** El consumidor pide datos cuando está listo. Es más seguro ante sobrecargas (evita saturación).

## 5. Pipelines de "Caja Negra" vs Transparentes
Un buen diseño senior incluye **Checkpoints**. Cada X etapas, guarda el estado actual en un almacenamiento persistente. Si el servidor explota, puedes retomar la pipeline desde el último checkpoint en lugar de empezar de cero con 10 millones de registros.

## Resumen: Dibujar antes de Programar
Antes de escribir una sola línea de `asyncio`, dibuja tu pipeline en un papel. Identifica los puntos de fallo, los cuellos de botella probables y dónde vas a poner los límites de memoria. Un buen diseño arquitectónico ahorra semanas de refactorizaciones dolorosas.
