# Gestión de Variables de Entorno en Compose

Nunca hardcodees secretos en el archivo `docker-compose.yml`. Si lo haces y subes el archivo a Git, has comprometido tu seguridad.

## 1. El archivo `.env`
Docker Compose busca automáticamente un archivo llamado `.env` en la misma carpeta.
```text
# Contenido del .env
DB_PASSWORD=super-secreto-123
DEBUG=True
```

En el `docker-compose.yml`, usa la sintaxis `${VARIABLE}`:
```yaml
services:
  db:
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
```

## 2. Inyección desde el Host
Si una variable está definida en tu terminal (`export DB_PASSWORD=xyz`), Compose le dará prioridad sobre el archivo `.env`. Esto es ideal para los pipelines de CI/CD.

## 3. El flag `env_file`
Si tienes muchas variables (ej: 50 settings de la App), no las enlistes una a una.
```yaml
web:
  env_file:
    - .env.production
```

## 4. Prioridad de Variables (Senior Check)
1. Valores puestos directamente en el `environment:` del YAML.
2. Variables del Shell (export).
3. El archivo `.env`.
4. Valores definidos en el `ENV` del Dockerfile.

## 5. Secretos de Docker (Avanzado)
Para un nivel de seguridad superior, usa `secrets:`. Esto no pasa la contraseña por variables de entorno (que son visibles en `docker inspect`), sino que monta un archivo temporal encriptado dentro del contenedor.

## Resumen: Aislamiento de Configuración
Un archivo YAML de Compose debe ser genérico. Toda la configuración específica del entorno (Dev vs Prod) debe estar en archivos `.env` o variables de shell, los cuales **NUNCA** deben subirse al repositorio de código.
