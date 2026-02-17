# Manejo de Fallos: Estrategias de Recuperación

Cuando los reintentos fallan y el error es definitivo, necesitas un protocolo claro de actuación para minimizar el impacto en el negocio.

## 1. Circuit Breaker (Disyuntor)
Si una fuente de datos está caída, no sigas intentando conectar cada segundo. El Circuit Breaker "abre el circuito" y detiene el pipeline durante un tiempo largo (ej: 1 hora) para dar tiempo a que el sistema se recupere.

## 2. Fallback (Plan B)
¿Existen datos alternativos que podamos usar?
- Si la API de tiempo de cambio de moneda falla, usa el último tipo de cambio que tengamos guardado en caché. No es perfecto, pero es mejor que tener 0 ventas.

## 3. Aislamiento (Blast Radius)
Diseña el sistema para que el fallo de un pipeline no rompa los demás.
- Usa colas diferentes.
- No compartas la misma base de datos de Staging para procesos que no tienen nada que ver.

## 4. El proceso de "Backfill" Manual
Cuando arregles el problema, tendrás un "agujero" de datos en las fechas del fallo.
- Tu pipeline debe permitir re-ejecutar rangos de fechas específicos para rellenar esos huecos una vez que la situación sea estable.

## 5. Post-Mortem: Aprender del error
Cada fallo crítico debe terminar en un documento de análisis:
- ¿Qué pasó?
- ¿Por qué el sistema no lo detectó antes?
- ¿Qué vamos a cambiar para que no vuelva a pasar? (Acciones preventivas).

## Resumen: Resiliencia no es Perfección
La resiliencia no es construir un sistema que nunca falle (eso no existe), sino construir uno que sepa cómo fallar de forma controlada y cómo recuperarse lo más rápido posible.
