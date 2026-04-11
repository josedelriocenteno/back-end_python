# HTTP Security Headers: La armadura invisible

Los headers de respuesta HTTP permiten que el servidor le dé órdenes de seguridad al navegador del usuario. Configurar estos headers correctamente reduce drásticamente ataques como XSS, Clickjacking y Sniffing.

## 1. Content-Security-Policy (CSP)
Es el más potente y complejo. Dice qué fuentes de contenido son de confianza.
- **Instrucción:** `default-src 'self'; script-src 'self' https://scripts.trusted.com;`
- **Evita:** Cross-Site Scripting (XSS), ya que el navegador se negará a ejecutar scripts de dominios no autorizados.

## 2. X-Frame-Options
Previene ataques de **Clickjacking** (meter tu web en un iframe invisible para engañar al usuario).
- **Valor recomendado:** `DENY` o `SAMEORIGIN`.

## 3. Strict-Transport-Security (HSTS)
Obliga al navegador a comunicarse solo por HTTPS durante un periodo de tiempo.
- **Instrucción:** `max-age=63072000; includeSubDomains; preload`
- **Evita:** Ataques de "downgrade" de HTTPS a HTTP.

## 4. X-Content-Type-Options
Evita que el navegador intente "adivinar" el tipo de contenido (MIME Sniffing).
- **Valor recomendado:** `nosniff`.
- **Por qué:** Evita que un atacante suba un archivo `.jpg` que en realidad contiene código JavaScript y el navegador lo ejecute.

## 5. Referrer-Policy
Controla cuánta información sobre el origen se envía en el header `Referer` al navegar a otro sitio.
- **Valor recomendado:** `strict-origin-when-cross-origin`.

## 6. Permissions-Policy
Limita qué funciones del navegador puede usar tu App (Cámara, Micrófono, Geolocalización).
- **Ejemplo:** `camera=(), microphone=(), geolocation=(self)`

## Implementación en FastAPI
```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

## Resumen: Un paso obligatorio
Muchos desarrolladores ignoran estos headers porque "no se ven", pero herramientas de auditoría como [Observatory de Mozilla](https://observatory.mozilla.org/) o [SecurityHeaders.io](https://securityheaders.com/) te darán una nota de Suspenso si no los usas.
