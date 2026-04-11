# Autenticación Básica (Basic Auth): Por qué NO usarla en producción

La Autenticación Básica es el método más simple definido por el protocolo HTTP. Aunque es útil para prototipos rápidos, tiene deficiencias graves que la hacen peligrosa para aplicaciones reales.

## 1. ¿Cómo funciona?
1. El cliente envía el header `Authorization: Basic [base64(usuario:password)]`.
2. El servidor decodifica el Base64 y comprueba las credenciales contra la base de datos.

## 2. Los grandes problemas
- **Exposición de Credenciales:** El usuario y la contraseña viajan en cada petición. Si la conexión no es HTTPS, cualquiera puede verlos.
- **Base64 NO es cifrado:** Cualquiera puede decodificarlo instantáneamente.
- **Sin Logout real:** El navegador suele recordar las credenciales de Basic Auth hasta que se cierra la sesión del navegador. Es muy difícil forzar un "Cerrar sesión" desde el servidor.
- **Incompatible con 2FA:** No hay lugar para introducir códigos de verificación de segundo factor de forma limpia.

## 3. Cuándo SÍ es aceptable
- Proteger una página de administración interna ultra-privada donde solo entran desarrolladores.
- Entornos de desarrollo locales donde el tráfico no sale a internet.
- Microservicios internos que se comunican por una red privada protegida (aunque incluso aquí, mTLS o API Keys son preferibles).

## Resumen: Una reliquia del pasado
En un mundo de APIs modernas, la Autenticación Básica debe evitarse en favor de **Tokens (JWT)** o **Sesiones seguras**. Entender sus debilidades es vital para no usarla por "pereza" en sitios donde la seguridad importa.
