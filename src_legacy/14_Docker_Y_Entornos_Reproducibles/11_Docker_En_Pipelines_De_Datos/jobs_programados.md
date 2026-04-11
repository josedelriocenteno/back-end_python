# Jobs Programados: Cron dentro y fuera de Docker

Muchas tareas de datos deben ejecutarse periódicamente (ej: limpiar logs cada noche a las 3:00 AM). Hay dos formas de abordar esto con Docker.

## 1. Cron en el Host (Recomendado)
El servidor tiene un `cron` normal que lanza un comando `docker run` o `docker compose up`.
- **Pro:** Muy simple y robusto. Si el contenedor muere, solo ha muerto ese job.
- **Contra:** Dependes de la configuración del servidor físico.

## 2. El Contenedor "Cron"
Un contenedor que corre siempre y tiene un daemon de `cron` interno que lanza scripts.
- **Pro:** Todo está autocontenido en Docker. No dependes del host.
- **Contra:** Tienes un proceso extra consumiendo RAM solo para esperar.

## 3. Orquestadores Modernos (Airflow / Prefect)
En entornos senior, no usamos Cron manual. Usamos orquestadores de DAGs.
- **DockerOperator:** Airflow lanza un contenedor de Docker por cada paso de tu pipeline. Esto es el estándar de oro de la industria.

## 4. El problema de los "Contenedores Huérfanos"
Si lanzas un job cada minuto y tarda 2 minutos en terminar, pronto tendrás el servidor lleno de contenedores acumulándose.
- **Solución:** Usa el flag `--rm` para que el contenedor se borre automáticamente al terminar.
```bash
docker run --rm mi_script_limpieza
```

## 5. Gestión de Timeouts
Un job programado puede quedarse colgado eternamente por un bloqueo en la red.
- **Solución:** Limita la vida del contenedor.
```bash
timeout 5m docker run --rm mi_job
```

## Resumen: Automatización Robusta
Elegir entre Cron de host u orquestadores depende de la complejidad de tu pipeline. En cualquier caso, Docker asegura que la tarea programada se ejecute siempre en un entorno limpio y controlado, minimizando el riesgo de fallos por "suciedad" de ejecuciones anteriores.
