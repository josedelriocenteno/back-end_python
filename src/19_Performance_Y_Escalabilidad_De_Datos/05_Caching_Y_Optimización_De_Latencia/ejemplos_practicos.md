# Ejemplos Prácticos de Caching

Vamos a ver tres casos reales donde la caché transforma por completo el rendimiento del sistema.

## Caso 1: API de Clima (API Gateway Cache)
Tu App llama a una API externa (ej: OpenWeather) para saber si llueve. Cada llamada cuesta dinero y tarda 500ms.
*   **Solución:** Cacheamos la respuesta por 10 minutos basada en la ciudad: `weather:{madrid}`.
*   **Impacto:** El 99% de los usuarios reciben la respuesta en 2ms (desde Redis) y la factura de la API externa se reduce drásticamente.

## Caso 2: Contador de "Likes" (Write Buffer)
En una red social, miles de personas dan "Like" por segundo. Actualizar la base de datos SQL en cada clic bloquearía las tablas.
*   **Solución:**
    1. Guardamos los clics en Redis usando un contador atómico: `INCR video:123:likes`.
    2. Cada 5 minutos, un proceso en segundo plano lee el total de Redis y hace UNA sola actualización masiva en la DB SQL.
*   **Impacto:** Escritura ultra-rápida y base de datos SQL descargada de trabajo inútil.

## Caso 3: Búsqueda de Productos (Result Set Cache)
Una query de búsqueda con filtros complejos (precio, categoría, stock, color) tarda 2 segundos.
*   **Solución:** Generamos un "Hash" de los parámetros de búsqueda (ej: `search_f8a92c`) y guardamos el resultado JSON en Redis por 1 minuto.
*   **Impacto:** Si dos usuarios buscan lo mismo (muy común), el segundo recibe el resultado al instante.

## La Regla de Oro del Caching
> "La mejor query es la que nunca llega a ejecutarse en la base de datos".

## Resumen: Optimización Inteligente
Cualquier parte del sistema que sea lenta, cara o repetitiva es candidata a ser cacheada. Desde APIs externas hasta contadores de actividad, la caché es la herramienta que permite a los sistemas modernos escalar a millones de usuarios manteniendo latencias de milisegundos.
