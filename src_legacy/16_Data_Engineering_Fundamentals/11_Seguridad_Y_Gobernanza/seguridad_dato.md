# Seguridad del Dato: Los 3 Pilares

La seguridad no es un "añadido" al final del proyecto. En ingeniería de datos, la seguridad debe estar integrada en cada tubería para proteger el activo más valioso de la empresa.

## 1. Confidencialidad: ¿Quién puede ver qué?
- **RBAC (Role-Based Access Control):** Definir permisos por roles (Analista, Data Scientist, Admin).
- **Row-Level Security (RLS):** Un analista de España solo puede ver filas donde `pais = 'ES'`.
- **Column-Level Security:** Ocultar columnas sensibles (ej: sueldo) a ciertos usuarios.

## 2. Integridad: ¿El dato es real?
- **Checksums:** Asegurar que los archivos no se han corrompido durante el viaje de S3 al Warehouse.
- **Inmutabilidad:** Los datos crudos (Bronze) nunca deben modificarse. Deber ser de solo lectura para evitar manipulaciones accidentales o malintencionadas.

## 3. Disponibilidad: ¿Está el dato cuando se necesita?
- **Backup & Recovery:** Planes de recuperación ante desastres en la región de la nube.
- **Failover:** Conmutación automática a un sistema secundario si el principal cae.

## 4. Auditoría (Audit Logs)
Debes registrar cada vez que alguien consulta o mueve datos sensibles. En caso de una filtración (Data Breach), el log de auditoría es lo único que permitirá saber qué se ha perdido y por quién.

## 5. El principio de "Privilegio Mínimo"
Un script de Python que solo extrae datos de una API no debería tener permisos de administrador en la base de datos. Dale solo el permiso mínimo necesario (`SELECT` sobre una tabla específica) para hacer su trabajo.

## Resumen: Blindar el Pipeline
Seguridad significa que un error humano o un ataque externo no destruyan la reputación de la compañía. Como Data Engineer, eres el guardián de la privacidad y la integridad de los datos de millones de usuarios.
