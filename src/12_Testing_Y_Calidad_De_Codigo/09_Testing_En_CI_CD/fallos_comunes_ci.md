# Fallos Comunes en el Entorno de CI

Es frustrante cuando un test pasa en tu local pero falla en la pipeline de CI/CD. Estos son los culpables más habituales y cómo un desarrollador senior los soluciona.

## 1. El entorno "Contaminado"
- **Problema:** En tu local tienes instalada una librería global o una configuración de sistema que no está en el servidor de CI.
- **Solución:** Trabaja siempre con entornos virtuales (`venv`) limpios y asegúrate de que todas tus librerías están en el archivo `requirements.txt` o `pyproject.toml`.

## 2. Diferencias de Sistema Operativo e Idioma
- **Problema:** Tú programas en Mac/Windows, pero el CI corre en Linux (Ubuntu). Las rutas de archivos (`/` vs `\`) o la codificación de caracteres cambian.
- **Solución:** Usa `pathlib` de Python para manejar rutas de forma agnóstica al SO. Configura el `LOCALE` en UTF-8 en tus scripts de CI.

## 3. Race Conditions en la Red
- **Problema:** En el servidor de CI, la red puede ser más lenta. Dos tests asíncronos que corren bien en local fallan por timeout en el CI.
- **Solución:** Aumenta ligeramente los timeouts en el entorno de CI y asegúrate de esperar correctamente a que los servicios de Docker (DB) estén listos antes de lanzar los tests (usando `wait-for-it.sh`).

## 4. Secretos y Variables de Entorno
- **Problema:** El test falla porque no encuentra la `SECRET_KEY` o la URL de la DB.
- **Solución:** Configura estos valores en los "Repository Secrets" de tu plataforma de CI. Nunca pongas claves reales en el código de test ni en el archivo YAML de configuración.

## 5. Falta de Aislamiento de Puerto
- **Problema:** Si intentas correr la base de datos en el puerto 5432 y el servidor de CI ya tiene algo ahí, el test fallará.
- **Solución:** Usa puertos dinámicos para tus contenedores de test o deja que Testcontainers elija un puerto libre automáticamente.

## Resumen: Debugging a ciegas
Cuando un test falle en el CI, el primer paso no es cambiar el código, es **leer los logs**. Si los logs no son suficientes, intenta recrear el entorno usando una imagen de Docker idéntica a la del CI. Un desarrollador senior diseña sus tests para que sean portables y resilientes a cambios en la velocidad del hardware.
