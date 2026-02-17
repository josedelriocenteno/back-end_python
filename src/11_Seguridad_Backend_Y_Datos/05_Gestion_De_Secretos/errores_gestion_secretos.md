# Errores en la Gestión de Secretos (Cómo NO hacerlo)

Incluso con las mejores herramientas, la complacencia o las prisas pueden llevar a fugas de secretos masivas. Estos son los errores que han costado millones a empresas reales.

## 1. Hardcoding (El pecado original)
- **Fallo:** Poner `api_key = "sk_test_51Mz..."` directamente en un archivo `.py`.
- **Realidad:** El código es eterno. Aunque lo borres en el siguiente commit, seguirá en el historial de Git para siempre.
- **Solución:** Si lo has hecho, debes **REVOCAR** la clave inmediatamente y generar una nueva. Borrarla del código no es suficiente.

## 2. Subir el archivo `.env` por error
- **Fallo:** Olvidar añadir el archivo al `.gitignore`.
- **Ataque:** Bots automáticos que clonan repositorios recién creados o actualizados buscando patrones de claves de AWS o bases de datos.
- **Solución:** Usa herramientas como `git-secrets` o `trufflehog` en tus máquinas de desarrollo para evitar que el commit se realice si detecta un secreto.

## 3. Enviar Secretos por Canales Inseguros
- **Fallo:** Pasar la contraseña de producción a un compañero por Slack, WhatsApp o Email.
- **Realidad:** Esos mensajes quedan guardados en servidores de terceros y en los dispositivos personales desprotegidos.
- **Solución:** Usa gestores de contraseñas corporativos (1Password, Bitwarden) o herramientas de "One-time secret" que autodestruyen el mensaje tras ser leído.

## 4. Reutilizar Secretos entre Entornos
- **Fallo:** Usar la misma clave de API de Stripe o la misma `SECRET_KEY` para Desarrollo, Staging y Producción.
- **Peligro:** Si un desarrollador junior comete un error en su local, podría borrar datos de la base de datos de producción o procesar pagos reales.
- **Regla de Oro:** Cada entorno debe tener sus propios secretos, totalmente aislados.

## 5. Falta de Rotación
- **Fallo:** Mantener la misma contraseña de base de datos durante 3 años.
- **Realidad:** Si la clave fue interceptada en algún momento, el atacante tiene 3 años para estudiar tu sistema sin que te des cuenta.
- **Solución:** Implementa una política de rotación (mínimo cada 90 días).

## 6. Permisos de "Solo Dios" (Over-privileged)
- **Fallo:** Usar el `Root User` de AWS para que la aplicación suba archivos a un S3.
- **Solución:** Crea un usuario con permisos limitados a SOLO esa acción en ese bucket específico.

## Resumen: La llave está en tus manos
La gestión de secretos es un ejercicio de disciplina. No atajes camino por ir más rápido hoy, porque pagarás el precio con un hackeo mañana. La seguridad de los secretos es un proceso de "Cero Confianza" (Zero Trust).
