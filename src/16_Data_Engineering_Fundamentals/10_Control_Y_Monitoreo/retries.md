# Retries: La primera línea de resiliencia

En un mundo distribuido, la red y los sistemas externos fallarán. Los **Retries** (Reintentos) automáticos evitan que problemas temporales se conviertan en desastres para el negocio.

## 1. El concepto
Si una tarea falla, el sistema intenta ejecutarla de nuevo automáticamente tras un breve periodo de tiempo.

## 2. Estrategias de Espera
- **Fixed Delay:** Esperar siempre lo mismo (ej: 10 segundos).
- **Exponential Backoff:** Esperar cada vez más (1s, 2s, 4s, 8s...). Es lo más profesional porque evita saturar a un sistema que ya está sufriendo.
- **Jitter (Ruido):** Añadir una pequeña cantidad de tiempo aleatorio para que, si 100 procesos fallan a la vez, no reintenten todos exactamente en el mismo milisegundo.

## 3. Límites de Reintento
Nunca reintentes infinitamente.
- **Tip:** Configura 3-5 reintentos. Si tras el 5º intento sigue fallando, es probable que no sea un error de red temporal, sino un bug o una caída mayor que requiere intervención humana.

## 4. Idempotencia y Reintentos
**REGLA DE ORO:** Solo puedes reintentar una tarea de forma segura si esa tarea es **Idempotente** (ver sección 03). Si tu tarea inserta datos sin comprobar si existen, los reintentos duplicarán la información.

## 5. Implementación en Orquestadores
Herramientas como Airflow permiten configurar esto en una sola línea:
```python
retries=3,
retry_delay=timedelta(minutes=5),
retry_exponential_backoff=True
```

## Resumen: Auto-sanación
Los reintentos automáticos son la diferencia entre un ingeniero que tiene que estar pendiente del móvil todo el fin de semana y uno que ha automatizado la resiliencia básica. Permite que el sistema absorba los "glitches" menores de la infraestructura.
