# JWT Deep Dive: Access vs Refresh Tokens

El uso de **JSON Web Tokens (JWT)** es el estándar de facto para APIs. Pero para un sistema realmente seguro, no basta con un solo token; necesitamos un ecosistema de tokens con diferentes responsabilidades.

## 1. Access Token (El pase de corta duración)
- **Vida:** 15 - 60 minutos.
- **Peligro:** Si te lo roban, el hacker tiene acceso total. Por eso debe morir pronto.
- **Contenido:** Suele llevar el `user_id`, `rol` y la `exp` (expiración).

## 2. Refresh Token (El seguro de vida)
- **Vida:** 7 - 30 días.
- **Uso:** Solo sirve para una cosa: pedir un nuevo Access Token. Se envía a un endpoint específico (`/token/refresh`).
- **Seguridad:** A diferencia del Access Token, este SÍ debe estar registrado en la base de datos para poder ser invalidado si el usuario cierra la sesión o si se detecta un robo.

## 3. El Flujo de Trabajo Profesional
1. El usuario se loguea. Recibe **Access** y **Refresh**.
2. Al minuto 16, el Access Token caduca. El servidor devuelve un **401**.
3. El frontend envía el **Refresh Token** al backend.
4. El backend verifica:
    - ¿La firma es válida?
    - ¿Sigue vivo (exp)?
    - ¿Está en nuestra DB y NO está marcado como revocado?
5. Si todo es OK, el backend devuelve un NUEVO **Access Token**.

## 4. Ventajas de esta arquitectura
- **Seguridad Dinámica:** Puedes revocar una sesión completa simplemente borrando el Refresh Token de la DB.
- **Experiencia de Usuario (UX):** El usuario no tiene que poner su contraseña cada 15 minutos; el proceso de refresco es invisible para él.
- **Stateless-ISH:** Mantienes la velocidad de JWT para el 99% de las peticiones, y solo consultas la DB el 1% de las veces (cuando el token se refresca).

## 5. El campo 'jti' (JWT ID)
Es una buena práctica añadir un ID único a cada token generado. Esto permite identificar un token específico incluso si los datos internos son idénticos. Es vital para auditoría y listas negras.

## Resumen: Diseña pensando en el robo
En seguridad, no preguntamos "SI" nos van a robar un token, sino "CUÁNDO". Los Access Tokens cortos limitan el daño, y los Refresh Tokens nos dan el botón del pánico para cortar el acceso.
