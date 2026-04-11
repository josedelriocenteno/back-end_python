# Reintentos y Gestión de Fallos en Pipelines

Las tuberías de datos fallan. Un servidor externo se cae, la DB se bloquea o un dato viene con un formato corrupto. Como desarrollador senior, tu pipeline debe ser capaz de sobrevivir a estos incidentes sin perder información.

## 1. Estrategia de Reintento (Retries)
No todos los errores son definitivos. Errores de red temporales (Timeout 504) deben reintentarse.
- **Exponential Backoff:** No reintentes inmediatamente. Espera 1s, luego 2s, luego 4s... Esto evita saturar más al servicio que ya está sufriendo.
- **Jitter (Ruido Aleatorio):** Añade un poco de tiempo al azar a los reintentos para evitar que miles de workers reintenten exactamente en el mismo milisegundo.

## 2. Colas de Errores (Dead Letter Queues - DLQ)
Si un dato falla tras N reintentos, **NUNCA lo borres.**
- **Acción:** Mueve ese dato a una cola especial de fallos (DLQ).
- **Propósito:** Permite que un humano revise el dato el lunes por la mañana, corrija el bug y vuelva a inyectar el dato en la pipeline.

## 3. El patrón "Circuit Breaker" (Disyuntor)
Si la base de datos ha fallado 50 veces seguidas, es tontería seguir intentándolo.
- El Circuit Breaker "abre el circuito" y detiene la pipeline durante 5 minutos para dar tiempo al sistema a recuperarse, enviando una alerta crítica al equipo.

## 4. Idempotencia: La Regla de Oro
Un dato puede procesarse dos veces (por un reintento tras un fallo a medias).
- Tu código debe ser **idempotente**: ejecutar la misma operación dos veces debe tener el mismo resultado que ejecutarla una sola vez.
- **Ejemplo:** En lugar de `UPDATE saldo = saldo + 10`, usa un ID de transacción para verificar si el abono ya se hizo.

## 5. Logging y Observabilidad
En una pipeline concurrente con miles de mensajes, un `print()` no sirve de nada.
- Usa **Correlation IDs**: Un ID único que acompañe al dato desde que entra hasta que sale, para que puedas buscar en los logs toda su historia si algo falla.

## Resumen: Resiliencia por Diseño
Una pipeline senior no es la que no falla, sino la que sabe qué hacer cuando el fallo ocurre. Capturar errores, reintentar con cabeza y salvar los datos corruptos en una DLQ es lo que separa un script de fin de semana de un sistema corporativo fiable.
