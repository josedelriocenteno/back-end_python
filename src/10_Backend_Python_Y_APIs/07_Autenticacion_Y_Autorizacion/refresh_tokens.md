# Refresh Tokens: Manteniendo al usuario conectado de forma segura

Un Access Token corto (ej: 30 minutos) es seguro porque si se roba, expira pronto. Pero es molesto para el usuario tener que loguearse cada media hora. Aquí entran los **Refresh Tokens**.

## 1. El ciclo de vida de los dos tokens

1.  **Login:** El servidor devuelve un `access_token` (30 min) y un `refresh_token` (7 días).
2.  **Uso:** El cliente usa el `access_token` para peticiones normales.
3.  **Expiración:** El `access_token` muere. El cliente recibe un 401.
4.  **Refresco:** El cliente envía el `refresh_token` a un endpoint especial `/refresh`.
5.  **Renovación:** El servidor valida el `refresh_token` y entrega un NUEVO `access_token`.

## 2. Diferencias de Seguridad

| Access Token | Refresh Token |
| :--- | :--- |
| Corta duración (minutos) | Larga duración (días/meses) |
| Se envía en CADA petición HTTP | Solo se envía al endpoint `/refresh` |
| Stateless (no se mira la DB) | **Stateful** (debe estar en la DB para poder revocarlo) |

## 3. ¿Por qué guardar el Refresh Token en la DB?
Si un usuario pierde su móvil o hackean su cuenta, necesitas una forma de invalidar su sesión.
*   **Access Token:** Es imposible de "borrar" porque no está en la DB del servidor (es stateless). Solo puedes esperar a que expire.
*   **Refresh Token:** Si lo tienes en tu base de datos, puedes borrarlo. La próxima vez que el hacker intente renovar, el servidor dirá "No tienes permiso" y la sesión se cerrará definitivamente.

## 4. Refresh Token Rotation
Para máxima seguridad, cada vez que el usuario usa un `refresh_token`, el servidor:
1.  Lo invalida.
2.  Le entrega un `refresh_token` totalmente nuevo.
*   **Ventaja:** Si un atacante roba un `refresh_token` y lo usa, y luego el usuario legítimo lo usa, el servidor detectará que se ha usado el mismo token dos veces y podrá cerrar TODAS las sesiones por seguridad (detección de brecha).

## 5. Almacenamiento en el Cliente (Frontend)
*   No guardes tokens en `LocalStorage` (vulnerable a XSS).
*   **Sugerencia senior:** Guarda el Refresh Token en una **Cookie HttpOnly, Secure y SameSite=Strict**. Así el código JavaScript no puede leerlo, solo el navegador puede enviarlo al servidor.

## Resumen: Equilibrio entre UX y Seguridad
Los Refresh Tokens permiten que tus usuarios no tengan que re-autenticarse constantemente sin comprometer la seguridad del sistema ante robos de tokens de corta duración.
