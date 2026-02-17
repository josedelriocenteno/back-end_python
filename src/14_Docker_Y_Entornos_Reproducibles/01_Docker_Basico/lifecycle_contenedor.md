# Ciclo de Vida de un Contenedor

Muchos errores de Docker ocurren porque intentamos hacer cosas a un contenedor que no está en el estado adecuado. Este es el camino que recorre un contenedor desde que nace hasta que muere.

## 1. Created (Creado)
Estado inicial tras un `docker create`. El contenedor existe, tiene su ID y recursos asignados, pero el proceso de Python todavía no ha arrancado.

## 2. Running (Corriendo)
El estado normal tras un `docker run` o `docker start`. El proceso principal (PID 1) está ejecutándose. Si este proceso termina o falla, el contenedor pasa a otro estado.

## 3. Paused (Pausado)
Estado tras `docker pause`. El contenedor se queda "congelado" en la RAM. No consume CPU pero los bytes siguen ahí. Útil para tareas de mantenimiento rápido sin perder el estado de la memoria.

## 4. Exited (Detenido)
El contenedor está parado. Puede haber sido por un `docker stop` controlado o porque la aplicación ha fallado (Crash). 
- **⚠️ Importante:** Los archivos modificados DENTRO del contenedor siguen ahí mientras no hagas un `docker rm`.

## 5. Restarting (Reiniciando)
Si has configurado una **Restart Policy** (ej: `--restart unless-stopped`), Docker detectará que el proceso ha muerto e intentará levantarlo automáticamente.

## 6. Removed (Eliminado)
Estado final tras `docker rm`. El contenedor desaparece del sistema y se libera todo el espacio de su capa de escritura.

## El Proceso PID 1: La Regla de Oro
Docker monitoriza el **proceso principal** que definiste en el CMD del Dockerfile.
- Si tu script de Python acaba con éxito, el contenedor muere con código 0.
- Si tu script explota, el contenedor muere con código de error.
- **ERROR COMÚN:** Lanzar procesos de fondo (background) y esperar que el contenedor siga vivo. Si el proceso principal termina, Docker cierra el contenedor inmediatamente.

## Resumen: Flujo Típico
`Pull Image` -> `Run (Created + Start)` -> `Stop` -> `Start` -> `Rm (Eliminado)`.
