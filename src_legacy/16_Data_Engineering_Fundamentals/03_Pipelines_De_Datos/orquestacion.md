# Orquestación: El director de orquesta del dato

Un pipeline real no es un solo script de Python. Son decenas de tareas (SQL, Python, Spark, Bash) que dependen unas de otras. La **Orquestación** gestiona estas dependencias.

## 1. ¿Qué hace un Orquestador?
- **Planificación (Scheduling):** Ejecutar tareas en fechas/horas específicas.
- **Gestión de Dependencias:** "No empieces el modelo de ML hasta que la limpieza de datos haya terminado con éxito".
- **Manejo de Fallos:** Reintentar tareas automáticamente si fallan.
- **Monitorización:** Una interfaz visual para ver el estado de todo el ecosistema de datos.

## 2. El concepto de DAG (Directed Acyclic Graph)
Es un plano de tus tareas:
- **Dirigido:** El flujo tiene un sentido (de la fuente al destino).
- **Acíclico:** No puede haber bucles infinitos (la tarea A no puede depender de la tarea B si B depende de A).

## 3. Orquestadores Modernos
- **Apache Airflow:** El estándar. Muy potente pero requiere gestionar servidores.
- **Prefect / Dagster:** Versiones más modernas centradas en la experiencia del desarrollador y en Python.
- **AWS Step Functions / Google Cloud Composer:** Opciones gestionadas en la nube.

## 4. Orquestación vs. Cron
Un `cron` es ciego. Solo ejecuta a una hora.
- Si la tarea de las 3:00 tarda más de una hora, la tarea de las 4:00 empezará de todos modos y puede que no tenga los datos listos.
- Un **Orquestador** sabe esperar. Si la tarea A tarda 2 horas, la tarea B esperará pacientemente a que A termine.

## 5. Tratar la Orquestación como Código
Define tus DAGs en archivos de Python. Esto permite versionarlos en Git, testearlos y tener un histórico claro de cómo ha evolucionado el flujo de datos de la empresa.

## Resumen: Control Total
La orquestación es el cerebro de la ingeniería de datos. Es lo que convierte scripts sueltos en un sistema industrial de procesamiento de información, fiable y transparente.
