# IAM: Identity and Access Management

IAM es el sistema que decide **quién** (identidad) puede hacer **qué** (permisos) sobre **qué recurso**. Es la base de la seguridad en Google Cloud.

## 1. Los 3 elementos de IAM
1. **Identidad (El "Quién"):** Un email de Google, un grupo de Google, o una Cuenta de Servicio (para máquinas).
2. **Rol (El "Qué"):** Un conjunto de permisos. No das permisos uno a uno; das "roles" que agrupan permisos (ej: "Lector de BigQuery").
3. **Recurso:** El objeto sobre el que se aplica el permiso (un cubo de S3, una tabla).

## 2. La "IAM Policy" (Enlace)
Una política es simplemente la unión de estos tres elementos:
- "El usuario `ana@empresa.com` tiene el rol `BigQuery Admin` en el proyecto `ventas-prod`".

## 3. Jerarquía y Herencia
Los permisos se heredan de arriba hacia abajo:
- Si das un permiso a alguien a nivel de **Organización**, ese usuario tiene el mismo permiso en todos los **Proyectos** de la empresa.
- **Tip Senior:** Intenta dar permisos siempre al nivel más bajo posible (recurso o proyecto) para evitar accesos accidentales a otros datos.

## 4. Tipos de Identidades
- **Google Accounts:** Usuarios individuales (`nombre@gmail.com` o `nombre@empresa.com`).
- **Google Groups:** Una colección de cuentas de Google. **Es la mejor práctica**: añade personas al grupo "Data Engineers" y dale los permisos al grupo, no a las personas individualmente.
- **Service Accounts:** Identidades para aplicaciones y scripts (las veremos en detalle en la sección 04).

## 5. Auditoría de Accesos
Google Cloud guarda un log cada vez que se concede o revoca un permiso. Como Data Engineer, debes revisar periódicamente quién tiene acceso a los sistemas para evitar "cuentas fantasma" de personas que ya no están en el equipo.

## Resumen: Control Total
IAM no es solo una herramienta administrativa; es la arquitectura que impide que un error humano borre accidentalmente la base de datos de producción o que un atacante robe los datos de tus clientes.
