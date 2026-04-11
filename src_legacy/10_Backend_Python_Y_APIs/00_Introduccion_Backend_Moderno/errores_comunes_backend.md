# Errores Comunes en el Desarrollo Backend

Aprender de los errores de otros es más barato que cometerlos tú mismo. Estos son los fallos más graves que vemos en APIs de producción.

## 1. El Monolito en el Controlador
*   **Error:** Poner validaciones, lógica de negocio y queries de SQL dentro de la función de la ruta (`def create_user`).
*   **Consecuencia:** Código imposible de testear y de leer.
*   **Solución:** Los controladores (routes) deben ser delgados. Delega la lógica a los **Servicios**.

## 2. Devolver Entidades de Base de Datos directamente
*   **Error:** Hacer `return db_user` (un modelo de SQLAlchemy).
*   **Consecuencia:** Expones campos sensibles (como el `password_hash`) o IDs internos que el frontend no necesita. Además, si cambias la DB, rompes el frontend.
*   **Solución:** Usa **Schemas de Salida (DTOs)** con Pydantic para filtrar qué datos salen de tu API.

## 3. Códigos de Estado Incorrectos
*   **Error:** Devolver siempre `200 OK`, incluso cuando hay un error, y poner el error en el JSON (`{"error": true}`).
*   **Consecuencia:** Los proxies, caches y librerías de cliente no pueden identificar fallos automáticamente.
*   **Solución:** Usa el estándar. `201` para creado, `400` para bad request, `404` para no encontrado, `500` para crash.

## 4. Ignorar la Seguridad de los Parámetros
*   **Error:** Confiar en que el cliente enviará el `user_id` correcto en el body de un UPDATE.
*   **Consecuencia:** Un usuario podría cambiar los datos de otro simplemente cambiando un número en el JSON (Vulnerabilidad Insecure Direct Object Reference - IDOR).
*   **Solución:** Valida siempre que el usuario autenticado tiene permisos sobre el recurso que está intentando modificar.

## 5. No gestionar el Timeout y la Concurrencia
*   **Error:** Ejecutar una tarea que tarda 30 segundos (ej: generar un PDF) de forma síncrona en el request.
*   **Consecuencia:** Bloqueas un worker del servidor y si 4 usuarios hacen lo mismo, tu API deja de responder.
*   **Solución:** Usa **Background Tasks** o colas de mensajes (Celery/Redis).

## 6. Falta de Documentación Viva
*   **Error:** Tener un documento PDF o Word con la documentación de la API.
*   **Consecuencia:** En cuanto cambias una línea de código, el documento queda obsoleto.
*   **Solución:** Confía en Swagger/OpenAPI, que se genera automáticamente desde el código.

## Resumen: Calidad desde el Día 1

Evitar estos anti-patrones te ahorra semanas de refactorización futura. Un backend senior no es el que arregla bugs rápido, sino el que no los introduce porque sigue principios de diseño sólidos.
