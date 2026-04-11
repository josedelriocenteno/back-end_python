# Errores Graves de Seguridad (Nivel Junior)

Todos hemos cometido fallos al empezar, pero en seguridad, algunos errores pueden ser terminales para un proyecto. Estos son los "pecados capitales" que debes detectar en cualquier Code Review.

## 1. Trusting the Client (Fiarte del frontend)
- **Fallo:** El frontend envía el `user_id` en el body de una petición de borrado y el backend lo usa directamente sin comprobar si ese usuario tiene permiso sobre ese ID.
- **Resultado:** Cualquier persona con Postman puede borrar a cualquier usuario de la base de datos.
- **Regla de Oro:** El backend NUNCA asume que el dato enviado por el cliente es "verdad". Siempre valida contra la sesión de usuario autenticada.

## 2. El archivo `.env` en el repositorio
- **Fallo:** Hacer `git add .` y subir las claves de API, contraseñas de DB y el `SECRET_KEY` de JWT a GitHub.
- **Resultado:** Bots escanean GitHub y en segundos tus servidores son hackeados.
- **Regla de Oro:** Añade `.env` al `.gitignore` desde el SEGUNDO CERO del proyecto.

## 3. Debug=True en Producción
- **Fallo:** Desplegar con el modo debug activado (ej: Django Debug Toolbar o los errores detallados de FastAPI).
- **Resultado:** Cuando ocurre un error, la API le muestra al atacante la estructura de tus archivos, versiones de librerías y fragmentos de código fuente.
- **Regla de Oro:** Los errores en producción deben ser opacos ("Algo ha ido mal"), mientras que los logs internos deben ser detallados.

## 4. Contraseñas en "Plain Text" (Texto Plano)
- **Fallo:** Guardar la contraseña tal cual la envía el usuario en una columna de texto en la DB.
- **Resultado:** Si la DB se filtra, todos los usuarios quedan expuestos instantáneamente.
- **Regla de Oro:** **Hashea** siempre las contraseñas con sal (Salt) usando algoritmos lentos como Bcrypt o Argon2.

## 5. Inexistencia de Rate Limiting
- **Fallo:** Dejar el endpoint `/api/login` abierto a infinitos intentos.
- **Resultado:** Ataques de fuerza bruta de diccionario que eventualmente darán con alguna contraseña débil.
- **Regla de Oro:** Limita los intentos fallidos por IP o por usuario.

## 6. Logs con Información Sensible
- **Fallo:** Loguear todo el request body, incluyendo el campo `password` o el `access_token`.
- **Resultado:** Los administradores de sistemas tienen acceso a las contraseñas de los usuarios simplemente leyendo los logs de texto.
- **Regla de Oro:** Filtra y oculta (Mask) campos sensibles antes de enviarlos al sistema de logging.

## Resumen: Humildad y Estándares
El error más grande es creer que puedes "hacerlo tú mismo" mejor que los estándares. No inventes tu propio sistema de cifrado, no hagas tus propios controladores de archivos si hay librerías seguras ya testeadas. Sigue las mejores prácticas y tu código será mucho más resistente.
