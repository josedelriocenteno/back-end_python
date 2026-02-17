# ¿Qué es la Observabilidad?

La **Observabilidad** es la capacidad de entender el estado interno de un sistema basándose únicamente en sus salidas externas (logs, métricas y trazas). 

No se trata solo de saber si el sistema está "vivo" o "muerto", sino de poder explicar **por qué** está ocurriendo un comportamiento extraño sin necesidad de entrar a la máquina y depurar el código manualmente en producción.

## Los 3 Pilares de la Observabilidad

1.  **Logs (Registros):** Eventos discretos con marca de tiempo. Son el relato detallado de lo que ocurrió (ej: "Error al conectar a la DB a las 10:05").
2.  **Métricas:** Datos numéricos agregados en el tiempo. Nos dicen el "cuánto" (ej: "La CPU está al 85%", "Hay 500 peticiones por segundo").
3.  **Trazas (Tracing):** El seguimiento de una petición a través de múltiples servicios. Nos muestra el camino y el tiempo que tardó cada paso.

## ¿Por qué es diferente para un Data Engineer?

En el desarrollo de software tradicional, la observabilidad se centra en la salud del servidor. Para nosotros, se añade una dimensión crítica: **la salud del dato**.

*   ¿Ha llegado el archivo a tiempo?
*   ¿El volumen de filas es el esperado?
*   ¿Ha cambiado el esquema de la tabla de origen sin avisar?

## Propiedades de un Sistema Observable

*   **Sin puntos ciegos:** Sabemos qué pasa en cada fase del pipeline.
*   **Contextual:** Un error de log incluye el ID de la transacción para poder rastrearlo.
*   **Predictiva:** Las métricas nos avisan ANTES de que el sistema falle por falta de memoria.

## Resumen: Luz en la caja negra
Sin observabilidad, gestionar una infraestructura de datos es como conducir a oscuras. La observabilidad enciende las luces y nos permite operar con confianza y responder rápidamente a los imprevistos.
