# Errores Comunes al Documentar APIs

Una mala documentación es casi tan inútil como ninguna. Estos son los fallos que hacen que tu API sea difícil de usar y aumenten la carga de soporte.

## 1. Ejemplos Inútiles o Genéricos
*   **Error:** Poner `{"id": 1, "name": "string"}` como ejemplo de usuario.
*   **Impacto:** El frontend no sabe qué formato real tiene el nombre, si hay espacios, si el ID es numérico o UUID en realidad.
*   **Solución:** Usa datos verosímiles: `{"id": 5421, "name": "Marta García"}`.

## 2. Ignorar los Errores (4xx y 5xx)
*   **Error:** Documentar solo el caso de éxito (200 OK).
*   **Impacto:** Cuando al frontend le llega un 400 Bad Request, no sabe qué ha pasado ni cómo manejarlo.
*   **Solución:** Define los esquemas de error comunes (401, 403, 404, 422) en la documentación de cada endpoint.

## 3. Discrepancia entre Código y Docs
*   **Error:** Actualizar el nombre de un campo en la DB pero olvidar actualizar el `examples` o el `description` en el Schema.
*   **Impacto:** Pérdida total de confianza del equipo externo.
*   **Solución:** Revisa los docs automáticos de Swagger en cada cambio.

## 4. No usar Tags (El "Muro de Endpoints")
*   **Error:** Tener 50 endpoints todos seguidos sin categorías.
*   **Impacto:** Nadie encuentra lo que busca.
*   **Solución:** Agrupa por recursos: `Users`, `Auth`, `Payments`, `Admin`.

## 5. Descripciones Crípticas
*   **Error:** Endpoint: `POST /p`. Descripción: `Procesa`.
*   **Impacto:** Frustración absoluta.
*   **Solución:** Sé descriptivo. ¿Qué se procesa? ¿Cuánto tarda? ¿Qué efectos secundarios tiene?

## 6. Ocultar la Autenticación
*   **Error:** Crees que añadiendo una dependencia `Depends(check_token)` es suficiente.
*   **Fallo:** Si no configuras `OAuth2PasswordBearer`, el botón "Authorize" de Swagger no aparecerá y nadie sabrá cómo autenticarse para probar la API.

## Resumen: Empatía con el Consumidor
Recuerda que tú sabes cómo funciona tu código porque lo escribiste, pero el otro desarrollador solo tiene la documentación. Si a ti te gustaría que te trataran con ejemplos claros y descripciones detalladas, haz lo mismo con tu API.
