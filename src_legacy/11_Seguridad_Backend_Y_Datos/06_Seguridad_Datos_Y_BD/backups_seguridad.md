# Backups de Seguridad: Tu última oportunidad

Un plan de seguridad que no incluya backups es simplemente un castillo de naipes esperando el viento. Los backups no son solo "copiar archivos", son un proceso de garantía de supervivencia.

## 1. La Regla del 3-2-1
- **3** copias de tus datos (Producción + 2 backups).
- **2** soportes diferentes (ej: Un disco sólido y un almacenamiento en la nube S3).
- **1** copia fuera de tu oficina/región (Off-site). Si se quema el datacenter de AWS en Irlanda, tu backup debe estar en AWS Virginia.

## 2. Tipos de Backup
- **Full Backup:** Copia completa de la DB. Lento pero fiable.
- **Incremental:** Solo guarda lo que ha cambiado desde el último backup. Rápido y ahorra espacio.
- **PITR (Point-In-Time-Recovery):** El nivel Senior. Guarda todos los logs de transacciones (`WAL` en Postgres). Permite restaurar la base de datos exactamente a como estaba a las 14:03:52 (ideal tras un borrado accidental masivo).

## 3. Seguridad del Backup
Un backup es una mina de oro para un atacante.
- **Cifrado Obligatorio:** Si tu backup no está cifrado, acabas de crear un agujero de seguridad masivo. Alguien que no pueda entrar en tu DB entrará en tu S3 y se llevará el backup.
- **Inmutabilidad:** Configura tus backups para que no se puedan borrar ni modificar durante X días (Object Lock). Esto evita que el Ransomware borre tus copias de seguridad antes de cifrar tu DB principal.

## 4. El Gran Error: No testear la restauración
Un backup que no se ha probado restaurar es un archivo que puede estar corrupto.
- **Paso Senior:** Automatiza un proceso que una vez al mes tome el último backup, lo levante en un servidor de test vacío y verifique que las tablas tienen datos coherentes.

## 5. Backups de Configuración
No solo copies la DB. Debes tener copias de:
- Tus scripts de despliegue.
- Tus variables de entorno (bien protegidas).
- Los archivos subidos por los usuarios (S3 Buckets).

## Resumen: No es si pasará, es cuándo
En el backend, las cosas fallan. Los discos mueren, los hackers entran y los desarrolladores cometen errores catastróficos. Un backup sólido y probado es lo único que separa un "mal día de trabajo" de un "despido masivo por pérdida de empresa".
