# Gestión de Secretos y Variables de Entorno

En Docker, la visibilidad de las variables es mayor de lo que parece. Como desarrollador senior, debes proteger los secretos (claves de API, passwords) de miradas indiscretas.

## 1. El peligro de `docker inspect`
Si pasas una contraseña con `-e MY_PASS=xyz`, cualquiera con acceso al comando `docker` puede verla ejecutando un `inspect`.
- **Solución:** En entornos críticos (Producción), usa **Docker Secrets** o monta archivos temporales de solo lectura con las claves.

## 2. Nunca uses `ENV` para secretos en el Dockerfile
Los valores definidos con `ENV` se graban en las capas de la imagen. 
- **Peligro:** Aunque borres la variable en una capa posterior, el secreto sigue estando en el historial de la imagen. Cualquiera que descargue la imagen puede hackearla.

## 3. Uso de archivos `.env` seguros
- **Local:** Usa `.env` y asegúrate de que esté en el `.gitignore`.
- **Producción:** Las variables se inyectan a través del orquestador (Kubernetes / ECS) o un servicio de Vault, nunca mediante archivos subidos al servidor.

## 4. Diferencia entre ARG y ENV
- `ARG`: Variables usadas **durante la construcción (build)** de la imagen. No están disponibles cuando el contenedor corre. Útil para versiones de librerías.
- `ENV`: Variables disponibles **mientras el contenedor corre**. Útil para configuraciones de la App.

## 5. El patrón de "Archivos de Secreto"
Muchas imágenes oficiales (como la de Postgres) permiten usar el sufijo `_FILE` en las variables.
- `POSTGRES_PASSWORD_FILE=/run/secrets/db_password`
- Esto le dice a la App: "No busques la contraseña en el entorno, búscala dentro de este archivo". Es mucho más seguro.

## Resumen: Invisible por defecto
Un secreto solo debe ser conocido por quien lo necesita. Minimiza el número de personas y procesos que pueden leer tus variables de entorno y usa herramientas de gestión de secretos profesionales siempre que sea posible.
