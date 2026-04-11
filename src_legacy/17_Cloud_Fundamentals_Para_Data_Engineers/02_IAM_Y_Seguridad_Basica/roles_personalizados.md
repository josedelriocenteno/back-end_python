# Roles Personalizados y Mínimo Privilegio

A veces los roles predefinidos son todavía demasiado amplios. Para una seguridad máxima, creamos **Roles Personalizados** (Custom Roles).

## 1. El Principio de Mínimo Privilegio (PoLP)
Es la regla de oro de la seguridad: "Cada usuario o servicio debe tener **solo** los permisos estrictamente necesarios para su tarea, y durante el tiempo mínimo indispensable".
- Si un script solo necesita leer el archivo `ventas.csv`, no le des permiso para ver todo el Bucket.

## 2. ¿Qué es un Rol Personalizado?
Es una lista de permisos individuales elegidos por ti.
- **Permisos:** Tienen un formato como `servicio.recurso.accion` (ej: `bigquery.tables.getData`).
- Creas un rol llamado "Lector de Ventas" y le añades solo los 3-4 permisos que necesita.

## 3. Limitaciones de los Roles Personalizados
- **Mantenimiento:** Si Google añade una funcionalidad nueva a un servicio, tu rol no se actualizará solo. Deberás añadir el permiso manualmente.
- No todos los servicios admiten roles personalizados (aunque el 99% de los de Data sí).

## 4. Auditoría con IAM Recommender
Google usa IA para analizar qué permisos usa realmente la gente.
- Si le diste permisos de Admin a un usuario pero en los últimos 90 días solo ha leído tablas, el **IAM Recommender** te dirá: "Oye, este usuario tiene demasiados permisos, cámbialo a Data Viewer". ¡Hazle caso!

## 5. Cuándo usar Roles Personalizados
- En entornos altamente regulados (Banca, Salud).
- Para cuentas de servicio críticas que tienen acceso a datos muy sensibles.
- Para evitar que los usuarios puedan ver configuraciones técnicas del proyecto que no necesitan.

## Resumen: Seguridad a medida
Dominar los roles personalizados y el principio de mínimo privilegio es lo que separa a un administrador de sistemas de un Arquitecto de Seguridad Cloud. Menos permisos significa menos riesgo.
