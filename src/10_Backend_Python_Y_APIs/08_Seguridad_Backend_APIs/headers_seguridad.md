# Headers de Seguridad HTTP: Blindando la Respuesta

A menudo olvidamos que las cabeceras que el servidor envía de vuelta al cliente son fundamentales para activar protecciones integradas en los navegadores modernos.

## 1. Content-Security-Policy (CSP)
Le dice al navegador de dónde tiene permitido cargar scripts, imágenes o estilos.
*   **Protección contra:** Ataques XSS (Cross-Site Scripting).
*   **Ejemplo:** `default-src 'self'; script-src 'self' https://trustedscripts.com`.

## 2. X-Frame-Options
Evita que tu web (o API si tiene docs) sea embebida en un `<iframe>` de otro sitio malicioso.
*   **Protección contra:** Clickjacking (hacer que el usuario pulse un botón invisible de tu sitio pensando que pulsa otro).
*   **Valor recomendado:** `DENY` o `SAMEORIGIN`.

## 3. Strict-Transport-Security (HSTS)
Obliga al navegador a comunicarse solo por HTTPS, incluso si el usuario intenta entrar por HTTP.
*   **Protección contra:** Downgrade attacks y Sniffing.
*   **Ejemplo:** `max-age=63072000; includeSubDomains`.

## 4. X-Content-Type-Options: nosniff
Evita que el navegador intente "adivinar" el tipo de contenido si este falta. Un atacante podría subir un archivo de texto con código malicioso y engañar al navegador para que lo ejecute como JavaScript.
*   **Valor:** `nosniff`.

## 5. Referrer-Policy
Controla cuánta información se envía al hacer clic en un enlace hacia otro sitio.
*   **Valor recomendado:** `strict-origin-when-cross-origin`. Evita que se filtren parámetros sensibles de la URL de tu API.

## Cómo implementarlo en FastAPI
Puedes usar middlewares globales para inyectar estos headers en cada respuesta:
```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

## Resumen: Configuración "Default Secure"
Tu API debe ser segura por defecto. Configurar estas cabeceras es una tarea de "una sola vez" que reduce drásticamente la superficie de ataque de tu frontend y protege la integridad de tus datos.
