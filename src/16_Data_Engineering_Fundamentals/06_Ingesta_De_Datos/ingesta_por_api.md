# Ingesta por API: Conectando con el SaaS

Extraer datos de APIs REST es una tarea diaria del Data Engineer. Requiere un manejo exquisito del protocolo HTTP y de la resiliencia ante errores de red.

## 1. Autenticación Profesional
Nunca guardes el Token en el código.
- Usa **Variables de Entorno**.
- Implementa lógica de refresco automático si el Token (JWT) caduca durante una sesión larga de descarga.

## 2. Paginación: El arte de bajar por trozos
La mayoría de APIs no te dan un millón de registros de golpe. Te dan 100 y un enlace a la página siguiente.
- **Técnica:** Crea un bucle que siga el enlace `next_page` hasta que esté vacío.
- **Cuidado:** Si la API tiene límites (Rate Limits), añade un `time.sleep()` entre páginas para que no te bloqueen la IP.

## 3. Manejo de Errores y Reintentos
La red fallará. Un error 500 no debe matar tu pipeline.
- Implementa **Exponential Backoff**: Si falla, espera 1 segundo. Si falla de nuevo, 2s, luego 4s... hasta un máximo de N intentos.

## 4. Ingesta Incremental por API
¿Cómo bajar solo los pedidos nuevos desde ayer?
- Consulta la API usando filtros: `GET /orders?min_date=2024-03-14T00:00:00Z`.
- Guarda en tu base de datos la fecha del último registro bajado para usarla como filtro en la siguiente ejecución (Patrón **Checkpoint**).

## 5. Herramientas de Ingesta (No reinventes la rueda)
Antes de escribir un script Python desde cero, mira si herramientas como **Airbyte** o **Fivetran** ya tienen un conector para esa API. Ahorrarás cientos de horas de mantenimiento.

## Resumen: Robustez HTTP
La ingesta por API es impredecible. Tu código debe ser defensivo, respetuoso con los límites del servidor y capaz de retomar la descarga donde se quedó si hay un corte de conexión.
