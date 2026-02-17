# OWASP API Security Top 10: Referencia de Backend

La organización OWASP mantiene una lista de las 10 amenazas más peligrosas para las APIs. Como desarrollador senior, estas 10 categorías deben ser tu "Padre Nuestro" de la seguridad.

## 1. BOLA (Broken Object Level Authorization)
El atacante accede a recursos que no le pertenecen manipulando IDs en la URL.
- **Ejemplo:** `/api/v1/orders/123` cambiandolo a `/124`.
- **Defensa:** Valida siempre si el usuario actual es el dueño del recurso `124`.

## 2. Broken User Authentication
Mecanismos de autenticación débiles (tokens que no expiran, passwords sin hashear, no MFA).
- **Defensa:** Usa JWT con tiempos de expiración cortos y algoritmos robustos.

## 3. Excessive Data Exposure
El backend devuelve más datos de los necesarios, confiando en que el frontend los oculte.
- **Ejemplo:** Devolver todo el objeto `User` incluyendo el hash del password.
- **Defensa:** Usa Schemas de Pydantic específicos para la salida (`response_model`).

## 4. Lack of Resources & Rate Limiting
No limitar el número de peticiones o el tamaño de la carga.
- **Defensa:** Implementa Rate Limiting por IP/Usuario y limita el tamaño del body.

## 5. Broken Function Level Authorization
Permitir que usuarios normales ejecuten funciones de admin (ej: `/api/admin/delete_all`).
- **Defensa:** Verifica roles y permisos específicos en CADA endpoint.

## 6. Mass Assignment
Permitir que el usuario envíe campos que no debería poder tocar.
- **Ejemplo:** Enviar `{"is_admin": true}` en un registro de usuario normal.
- **Defensa:** Define explícitamente qué campos puede recibir cada modelo Pydantic.

## 7. Security Misconfiguration
Configuraciones por defecto, headers inseguros o errores detallados en producción.
- **Defensa:** Automatiza el hardening y oculta los detalles de error.

## 8. Injection (SQL, NoSQL, Command)
Inyectar código malicioso en las entradas del usuario.
- **Defensa:** Usa queries parametrizadas y validadores de input.

## 9. Improper Assets Management
Desplegar versiones de prueba o APIs antiguas desprotegidas (`/v1`, `/v2-beta`).
- **Defensa:** Mantén un inventario de APIs y apaga las obsoletas.

## 10. Insufficient Logging & Monitoring
Ser hackeado y no enterarte hasta meses después.
- **Defensa:** Implementa logs estructurados y alertas en tiempo real de fallos de seguridad.

## Resumen: La base de la auditoría
Cuando alguien te diga "¿Es nuestra API segura?", tu respuesta debe basarse en estos 10 puntos. Si puedes demostrar cómo mitigas cada uno de ellos, eres un profesional de confianza.
