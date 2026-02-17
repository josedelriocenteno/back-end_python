# Revocación de Tokens: El Logout Real en APIs

Uno de los mitos de JWT es que "no se pueden revocar". Esto es falso. Aunque la validación de firma es descentralizada, la gestión de revocación debe ser centralizada para una seguridad real.

## 1. El problema del Logout en JWT
Si un usuario cierra sesión, el frontend borra el token de su memoria. ¡Genial! Pero si un atacante capturó ese token antes, el servidor lo seguirá aceptando hasta que caduque (ej: dentro de 30 minutos).

## 2. Estrategia A: Revocación por Refresh Tokens
Es la más sencilla. Simplemente borras el **Refresh Token** de la base de datos.
- El atacante puede seguir usando el Access Token actual por unos minutos, pero nunca podrá renovarlo. La sesión morirá de forma natural en breve.

## 3. Estrategia B: Blacklisting (Lista Negra)
Si necesitas invalidar un Access Token **al instante**, debes guardar el `jti` (ID del token) en una lista negra.
1. Cuando un usuario hace Logout, envías el token a `/auth/logout`.
2. El servidor extrae el `jti` y lo guarda en **Redis** con un tiempo de vida (TTL) igual al tiempo que le quedaba para caducar.
3. En CADA petición, el middleware de FastAPI comprueba: `Redis.exists(token_jti)`.
- **Desventaja:** Tu sistema deja de ser 100% Stateless. Ahora cada request requiere una consulta rápida a Redis.

## 4. Estrategia C: Invalidation por fecha (Global Logout)
Útil cuando el usuario cambia la contraseña o decide "Cerrar sesión en todos los dispositivos".
1. Guardas en la DB del usuario un campo `tokens_valid_after = datetime.now()`.
2. El middleware de JWT rechaza cualquier token cuya fecha de creación (`iat`) sea anterior a esa fecha.
- Esto invalida miles de tokens en un solo paso sin saturar la memoria.

## 5. El botón del Pánico (Kill Switch)
Como desarrollador senior, deberías proveer una forma de invalidar todos los tokens de todos los usuarios en caso de una filtración masiva del `SECRET_KEY`. Esto se logra simplemente cambiando el `SECRET_KEY` del servidor (aunque esto obligará a TODOS a loguearse de nuevo).

## Resumen: Elige tu nivel de rigor
Si tu app maneja dinero o salud, necesitas **Blacklisting** (Estrategia B). Para apps de consumo normal, la **Revocación de Refresh Tokens** (Estrategia A) es un equilibrio perfecto entre rendimiento y seguridad.
