# OWASP API Security Top 10: Los 10 Fallos más Críticos

OWASP es la autoridad global en seguridad web. Su lista "Top 10" es el manual de lo que **NO** debes hacer en tu backend.

## 1. Broken Object Level Authorization (BOLA/IDOR)
*   **El Fallo:** Acceder a `GET /orders/123` y que el servidor te devuelva el pedido aunque seas el usuario 4 y el pedido sea del usuario 5.
*   **Solución:** Valida siempre la propiedad del recurso en la DB: `WHERE id = 123 AND user_id = current_user_id`.

## 2. Broken Authentication
*   **El Fallo:** Esquemas de autenticación débiles que permiten adivinar tokens o fuerza bruta en logins.
*   **Solución:** Usa estándares (OAuth2/JWT) y protege los endpoints de login con Rate Limiting.

## 3. Excessive Data Exposure
*   **El Fallo:** El backend devuelve todo el perfil del usuario (incluyendo SSN o password_hash) y espera que el frontend lo filtre.
*   **Solución:** Usa Schemas (Pydantic/DTOs) de salida para enviar SOLO lo necesario.

## 4. Lack of Resources & Rate Limiting
*   **El Fallo:** Permitir que alguien pida `limit=1000000` registros o que suba archivos de 10GB.
*   **Solución:** Pon límites de tamaño de request y de paginación.

## 5. Broken Function Level Authorization
*   **El Fallo:** El backend asume que porque el endpoint no está en el menú de la App, nadie lo llamará. Un usuario puede probar a llamar a `DELETE /users/1` y el servidor lo ejecuta.
*   **Solución:** Implementa RBAC (Roles) en cada ruta administrativa.

## 6. Mass Assignment
*   **El Fallo:** Permitir al usuario enviar un JSON con `{"is_admin": true}` y guardarlo directamente en la DB.
*   **Solución:** No uses el mismo modelo para recibir datos que para guardar en DB. Define campos permitidos.

## 7. Security Misconfiguration
*   **El Fallo:** Dejar el modo Debug activado en producción o usar claves por defecto.
*   **Solución:** Automatiza tu configuración con variables de entorno y desactiva Swagger en producción si es una API interna.

## 8. Injection (SQL, Command, NoSQL)
*   **El Fallo:** Confiar en la entrada del usuario y concatenarla en una query.
*   **Solución:** Usa ORMs o queries parametrizadas.

## 9. Improper Assets Management
*   **El Fallo:** Dejar una versión antigua de la API (`/v1`) activa con fallos de seguridad conocidos.
*   **Solución:** Documenta y apaga versiones antiguas.

## 10. Insufficient Logging & Monitoring
*   **El Fallo:** Sufrir un ataque y no enterarte hasta que los datos están en el mercado negro.
*   **Solución:** Implementa logs detallados y alertas en tiempo real.

## Resumen: Tu Checklist de Seguridad
Cada vez que diseñes un nuevo endpoint, pasa esta lista de 10 puntos. Si puedes marcar todos con un "Protegido", tienes un backend robusto.
