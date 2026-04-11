# Rate Limiting: Protegiendo la Disponibilidad

El Rate Limiting consiste en limitar cuántas veces un cliente puede llamar a tus endpoints en un periodo de tiempo. Sin esto, tu API es vulnerable a ataques de Denegación de Servicio (DoS) y fuerza bruta.

## 1. ¿Por qué es vital?
- **Evitar Abusos:** Evita que un script mal programado o un atacante sature tus recursos.
- **Costes Cloud:** Si pagas por invocación (serverless) o por ancho de banda, el Rate Limiting protege tu cuenta bancaria.
- **Justicia (Fair Usage):** Asegura que un solo usuario pesado no degrade la experiencia de todos los demás.

## 2. Dónde implementar el límite
- **Capa de Red (WAF/Cloudflare):** El más eficiente. Bloquea el tráfico antes de que llegue a tu infraestructura.
- **Capa de Gateway (Nginx/Kong):** Muy rápido. Gestiona los límites antes de que el código Python se ejecute.
- **Capa de Aplicación (FastAPI + Redis):** El más flexible. Permite límites dinámicos (ej: usuarios Premium tienen 1000 req/min, usuarios Free solo 100).

## 3. Estrategias de Identificación
¿A quién limitamos?
- **Por IP:** Fácil, pero injusto si muchos usuarios comparten la misma IP (ej: una oficina o universidad).
- **Por API Key / Usuario:** Lo más preciso si la API es privada.
- **Por Atributo (Session ID):** Útil para usuarios no logueados pero identificables por cookie.

## 4. Respuesta Estándar
Cuando un usuario supera el límite, la API **DEBE** responder con:
- **Status Code:** `429 Too Many Requests`.
- **Header `Retry-After`:** Indica cuántos segundos debe esperar antes de reintentar.

## 5. Algoritmos comunes
- **Fixed Window:** Reinicia el contador cada minuto exacto. (Problema: picos en el borde del minuto).
- **Sliding Window:** Más suave. Calcula la tasa en una ventana de tiempo móvil.
- **Token Bucket:** Permite ráfagas cortas de tráfico pero mantiene una media constante.

## Resumen: No dejes la puerta abierta
Una API sin Rate Limiting es una bomba de relojería. Empieza con límites generosos y ajústalos según observes el tráfico real de tus usuarios.
