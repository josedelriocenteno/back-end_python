# Backpressure: Control de Flujo en Pipelines

El **Backpressure** (Presión de Retorno) es un concepto vital en la ingeniería de datos. Ocurre cuando una etapa de tu pipeline es mucho más lenta que la anterior, provocando que los datos se acumulen peligrosamente en la memoria.

## 1. El desastre de la "Cola Infinita"
Si tu `Extractor` genera 1.000 registros por segundo pero tu `Transformador` solo procesa 10:
- Los 990 registros restantes se guardan en la `Queue`.
- La memoria RAM del servidor empezará a subir sin control.
- Eventualmente, el proceso morirá por falta de memoria (OOM).

## 2. La solución: Colas con Límite (Bounded Queues)
En `asyncio.Queue(maxsize=10)`, si la cola llega a 10 elementos, el comando `await put()` se detendrá y **bloqueará al productor** hasta que el consumidor saque algún elemento.

## 3. Beneficios del Backpressure
- **Estabilidad:** La memoria RAM se mantiene constante y predecible.
- **Detección de Cuellos de Botella:** Al pausar al productor, ves claramente qué etapa es la que está frenando todo el sistema.
- **Sistemas Auto-regulados:** El sistema se adapta a la velocidad del recurso más lento (normalmente la base de datos).

## 4. Estrategias ante el bloqueo
Cuando el sistema se satura, tienes tres opciones senior:
1. **Wait (Esperar):** El productor se pausa (comportamiento por defecto de las colas limitadas).
2. **Drop (Tirar):** Si el dato no es crítico (ej: logs de monitorización), puedes descartar los datos nuevos.
3. **Scale (Escalar):** Levantar dinámicamente más workers para la etapa lenta.

## 5. El error del "Flush" manual
Evita intentar limpiar las colas a mano periódicamente. Confía en los mecanismos de bloqueo nativos de las librerías de concurrencia.

## Resumen: Equilibrio de Fuerzas
Un pipeline profesional no es el que más corre, sino el que mantiene un flujo constante y seguro. Implementar Backpressure evita caídas catastróficas y hace que tu backend sea resiliente ante picos inesperados de tráfico.
