# Gestión de Sesiones: Cookies vs Tokens

Una vez autenticado el usuario, ¿cómo recordamos quién es en las siguientes peticiones? Existen dos grandes arquitecturas en el backend moderno.

## 1. Sesiones Basadas en Cookies (Stateful)
Es el modelo tradicional de frameworks como Django o PHP.
- **Cómo funciona:** El servidor genera un `session_id`, lo guarda en su DB (o Redis) y envía una Cookie al cliente. En cada petición, el servidor consulta su DB para ver si ese ID sigue vivo.
- **Pros:** Fácil de invalidar (logout), muy seguro contra ataques XSS (con flag `HttpOnly`).
- **Contras:** Poco escalable (necesita sincronizar DB de sesiones en múltiples servidores), problemas con CORS y aplicaciones móviles.

## 2. Sesiones Basadas en Tokens / JWT (Stateless)
Es el modelo estándar de las APIs modernas y microservicios.
- **Cómo funciona:** El servidor genera un Token firmado que contiene los datos del usuario. El cliente guarda el token. El servidor NO guarda nada; simplemente valida la firma del token en cada petición.
- **Pros:** Totalmente escalable (no requiere DB), funciona perfecto con móviles y múltiples dominios.
- **Contras:** Difícil de invalidar antes de que expire (Logout complejo), riesgo de robo si se guarda mal en el frontend.

## 3. La Comparativa definitiva

| Característica | Cookies / Session | Tokens / JWT |
| :--- | :--- | :--- |
| **Almacenamiento Servidor** | Sí (DB/Redis) | No (Stateless) |
| **Escalabilidad** | Compleja | Excelente |
| **Invalidación inmediata** | Muy fácil | Difícil / Necesita lista negra |
| **Uso en Móvil** | Difícil | Nativo |

## 4. Prácticas de Seguridad en Sesiones
Independientemente del método:
- **Expiración:** Todas las sesiones deben morir tarde o temprano (Timeout).
- **Binding:** Vincular la sesión a la IP del usuario o al navegador (opcional pero más seguro).
- **Renovación:** Cambiar el ID de sesión tras un cambio de privilegios o login (evita Session Fixation).

## Resumen: Elige según tu Arquitectura
- Si estás haciendo una aplicación Web monolítica clásica: **Cookies**.
- Si estás haciendo una SPA (React/Vue) o una App Móvil: **Tokens/JWT**.
- Si eres Senior y quieres lo mejor de ambos: Usa **Tokens transmitidos en Cookies HttpOnly**.
