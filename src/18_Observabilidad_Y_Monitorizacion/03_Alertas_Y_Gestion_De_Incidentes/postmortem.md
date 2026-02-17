# Post-mortem: Aprendiendo del Desastre

Un **Post-mortem** es un documento y una reunión que ocurre DESPUÉS de que un incidente grave ha sido resuelto. Su objetivo no es buscar culpables, sino evitar que el fallo vuelva a ocurrir.

## 1. Cultura "Blameless" (Sin Culpas)
Esta es la regla más importante de la ingeniería moderna.
*   **MAL:** "El becario borró la tabla por error".
*   **BIEN:** "El sistema permitía borrar tablas de producción sin confirmación doble ni backups automáticos. Necesitamos mejorar la protección de la base de datos".
Si buscas culpables, la gente ocultará los errores. Si buscas soluciones, el sistema será cada vez más fuerte.

## 2. Partes de un Informe Post-mortem
*   **Resumen:** Qué pasó en 2 frases.
*   **Impacto:** Cuántos usuarios afectados y cuánto dinero/tiempo se perdió.
*   **Línea de Tiempo (Timeline):** 
    *   10:00 - El sistema falla. 
    *   10:05 - Suena la alerta.
    *   10:15 - El ingeniero empieza a investigar.
    *   10:45 - El fallo se identifica y se aplica el arreglo.
*   **Análisis Técnico:** ¿Por qué pasó? (Usa la técnica de los "5 Porqués").
*   **Acciones Correctivas (Action Items):** Lista de tareas concretas con un responsable asignado para que esto no pase nunca más.

## 3. Los "5 Porqués" (5 Whys) aplicados a Datos
*   1. ¿Por qué el dashboard estaba vacío? -> Porque la tabla no tenía datos nuevos.
*   2. ¿Por qué no había datos? -> Porque el pipeline de Airflow falló.
*   3. ¿Por qué falló? -> Porque el disco de la máquina se llenó.
*   4. ¿Por qué se llenó? -> Porque no borramos los logs temporales de hace un año.
*   5. ¿Por qué no los borramos? -> **Porque no teníamos configurada una política de ciclo de vida (Lifecycle Policy).**
*   **Acción final:** Configurar la política de borrar logs automáticamente.

## 4. Publicación y Transparencia
Comparte el Post-mortem con todo el equipo de ingeniería e incluso con otros departamentos si el impacto fue grande. Demuestra profesionalidad y compromiso con la calidad.

## 5. El valor del fallo
Un incidente sin post-mortem es una pérdida de tiempo. Un incidente con un buen post-mortem es una inversión en conocimiento que hace que tu infraestructura sea más resiliente y tu equipo más senior.

## Resumen: Ingeniería de la Resiliencia
El post-mortem es lo que separa a las empresas que viven en un caos constante de las que construyen sistemas sólidos. Trata cada error como una oportunidad gratuita de auditar y mejorar tus procesos y tu tecnología.
