# Rate Limiting: Protegiendo tu API de Abusos

Cualquier API pública está expuesta a ataques de denegación de servicio (DoS), ataques de fuerza bruta o simplemente usuarios que intentan "scrapear" tu base de datos de forma agresiva. El **Rate Limiting** es tu escudo.

## 1. ¿Qué es el Rate Limiting?
Es la práctica de limitar el número de peticiones que un cliente puede hacer en un periodo de tiempo determinado.
*   **Ejemplo:** Máximo 60 peticiones por minuto para usuarios gratuitos.

## 2. Niveles de Implementación

### A. Capa de Aplicación (FastAPI/Python)
*   **Pros:** Fácil de configurar, permite lógica compleja (ej: límites distintos por plan de suscripción).
*   **Contras:** Cada petición "consume" recursos de tu proceso Python antes de ser rechazada.
*   **Librería:** `slowapi`.

### B. Capa de Infraestructura (Recomendado)
*   **NGINX / Redis:** Rechazan la petición antes de que llegue a tu código.
*   **Cloudflare:** El estándar de la industria. Filtra el tráfico malicioso en el borde (Edge).

## 3. Códigos de Estado y Headers
Cuando un usuario excede el límite, debes responder con:
*   **Status Code:** `429 Too Many Requests`.
*   **Header `Retry-After`:** Indica al cliente cuántos segundos debe esperar antes de volver a intentarlo.

## 4. Estrategia de Identificación
¿Cómo sabemos quién es el cliente?
1.  **IP Address:** Fácil de implementar, pero problemática si muchos usuarios están tras la misma NAT (ej: una oficina).
2.  **API Key / Token JWT:** La forma más segura. El límite se aplica a la cuenta del usuario, no a su IP.

## 5. Algoritmos Comunes
*   **Fixed Window:** Resetea el contador cada minuto exacto. (Problema: picos al final del minuto).
*   **Sliding Window:** Más suave. El límite se calcula en base a los últimos 60 segundos rodantes.
*   **Token Bucket:** El usuario tiene una "cubeta" de permisos que se llena poco a poco. Permite ráfagas cortas (bursts) pero previene el abuso sostenido.

## Resumen: Disponibilidad para Todos
El Rate Limiting no es para castigar a los usuarios, sino para asegurar que el sistema sea estable y justo. Sin él, un solo usuario mal programado o malintencionado puede dejar fuera de servicio a todos los demás.
