# Perfiles y Entornos: Un YAML para todos

A veces quieres levantar solo la base de datos para ejecutar tests, otras veces quieres todo el stack con monitorización. Los **Perfiles de Compose** (introducidos en v2.0) son la solución.

## 1. Definición de Perfiles
```yaml
services:
  web:
    build: .
  
  db:
    image: postgres:15
  
  pgadmin:
    image: dpage/pgadmin4
    profiles:
      - tools # Este servicio NO arrancará por defecto
```

## 2. Uso en terminal
```bash
# Solo arranca web y db
docker compose up

# Arranca también las herramientas de monitorización
docker compose --profile tools up
```

## 3. Múltiples archivos YAML (Enfoque Clásico)
Otra estrategia es tener archivos separados que se sobreescriben:
- `docker-compose.yml` (Base: común a todo).
- `docker-compose.override.yml` (Dev: añade volúmenes para hot-reload).
- `docker-compose.prod.yml` (Prod: añade certificados SSL y quita modos debug).

```bash
# Levantar en producción mezclando dos archivos
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 4. ¿Cuándo usar cada uno?
- **Perfiles:** Para herramientas auxiliares (debuggers, visualizadores de DB, generadores de docs).
- **Archivos múltiples:** Para diferencias estructurales profundas entre el Local del desarrollador y el Servidor real.

## 5. El comando `config`
Si estás mezclando varios archivos y perfiles, es difícil saber qué va a pasar. Usa:
```bash
docker compose config
```
Esto te muestra el YAML resultante final antes de ejecutar nada.

## Resumen: Organización Senior
No dupliques código. Usa una base sólida de Compose y utiliza perfiles o overrides para adaptar el entorno a la necesidad del momento (Desarrollo, Test o Producción).
