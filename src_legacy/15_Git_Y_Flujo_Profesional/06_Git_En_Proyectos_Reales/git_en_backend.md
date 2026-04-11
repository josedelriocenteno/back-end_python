# Git en Backend: Gestión de APIs y Microservicios

El desarrollo de Backend tiene retos específicos en Git, especialmente cuando tratamos con migraciones de base de datos y despliegues sincronizados.

## 1. Migraciones de DB: El gran punto de conflicto
Varios desarrolladores creando migraciones (`001_add_user.py`, `002_add_admin.py`) al mismo tiempo.
- **Protocolo:** Si dos PRs añaden migraciones con el mismo número secuencial, habrá un conflicto en producción.
- **Solución:** Reasigna el número de migración tras hacer `rebase main` o usa herramientas que generen hashes únicos para los nombres de migración (ej: Alembic).

## 2. Variables de Entorno y Secretos
**Regla de Oro:** El `.env` NUNCA se sube a Git.
- Sube siempre un `.env.example` con las claves vacías para que el resto del equipo sepa qué variables necesita configurar.

## 3. Despliegue de Microservicios
¿Un solo repo para todos o uno por servicio?
- **Monorepo:** Facilita ver cambios que afectan a varios servicios. Requiere herramientas como Nx o Bazel para no testear todo en cada commit.
- **Multirepo:** Aislamiento total. Cada servicio escala y se versiona de forma independiente.

## 4. Git Tags para Versiones de API
Usa tags para marcar versiones estables de la API (`v1.4.2`). Esto permite que el equipo de Infraestructura sepa exactamente qué imagen de Docker desplegar.

## 5. El archivo `.dockerignore`
Es el hermano del `.gitignore`. Asegúrate de que no subes la carpeta `.git` dentro de la imagen de producción; no solo por espacio, sino por seguridad (un atacante podría descargar tu imagen y leer todo el historial del código).

## Resumen: Robustez y Trazabilidad
En Backend, Git es el registro de cómo ha evolucionado la lógica de negocio y el esquema de datos. Mantenerlo ordenado es fundamental para la estabilidad del sistema.
