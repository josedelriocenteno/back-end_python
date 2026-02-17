# Backups y Restore: Tu Seguro de Vida

En el mundo de las bases de datos, solo existen dos tipos de personas: las que han perdido datos y las que van a perderlos. La diferencia está en si tienen un backup que funcione.

## 1. Tipos de Backups en PostgreSQL

### A. SQL Dump (Lógico)
Exporta la estructura y los datos como un archivo de comandos SQL.
*   **Comando:** `pg_dump db_name > backup.sql`
*   **Pros:** Portable entre versiones de Postgres, fácil de leer y editar.
*   **Contras:** Lento en bases de datos gigantes (>100GB).

### B. File-System Level (Físico)
Copia directamente los archivos binarios de la base de datos.
*   **Comando:** `pg_basebackup`
*   **Pros:** Muy rápido de restaurar.
*   **Contras:** Solo funciona para restaurar en la misma versión de Postgres y sistema operativo.

### C. Point-In-Time Recovery (PITR)
Usa los archivos de log (WAL) para reconstruir la base de datos hasta un segundo exacto en el pasado.
*   **Escenario:** "Alguien borró una tabla a las 10:05 AM. Quiero recuperar la base de datos a las 10:04 AM".

## 2. Estrategias de Restauración (Restore)

Un backup no existe hasta que se prueba el restore.
```bash
# Restaurar un SQL dump
psql db_name < backup.sql
```

## 3. La Regla del 3-2-1

Es el estándar de oro de la seguridad:
*   **3** Copias de tus datos.
*   **2** Formatos o medios diferentes (ej: Disco local y Nube).
*   **1** Copia fuera de tus oficinas/centro de datos (Offsite).

## 4. Mejores Prácticas en Backend

1.  **Backups Automáticos:** Nunca dependas de un humano para hacer el backup. Usa cronjobs o las funciones del proveedor de nube (AWS RDS Snapshots).
2.  **Monitorización:** Recibe una alerta si el backup falla por falta de espacio o error en la red.
3.  **Probar el Restore:** Una vez al mes, intenta levantar una base de datos nueva con el backup de ayer. Si no funciona, tu backup es inútil.
4.  **Cifrado:** Los backups contienen todos los datos sensibles de tu app. Deben estar encriptados tanto en reposo como en tránsito.

## Resumen: Dormir Tranquilo

Los backups son la última línea de defensa ante errores humanos, desastres naturales o ataques de ransomware. Automatiza el proceso, diversifica las ubicaciones y, sobre todo, **practica la restauración**.
