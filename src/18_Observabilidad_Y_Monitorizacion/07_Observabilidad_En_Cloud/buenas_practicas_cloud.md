# Buenas Prácticas de Observabilidad en Cloud

Construir observabilidad en la nube requiere orden y estándares. Sigue estas reglas de oro para que tu monitorización en GCP sea de clase mundial.

## 1. Usa Etiquetas (Labels) en todo
Cada recurso de GCP (VM, Bucket, Dataset) debe tener etiquetas de organización:
*   `project=ventas`
*   `owner=equipo_data`
*   `env=prod`
Esto permite filtrar logs y métricas de forma masiva y automática.

## 2. Infraestructura como Código (IaC)
No crees las alertas y dashboards manualmente haciendo click en la consola.
*   Usa **Terraform**. Permite que tus alertas estén en Git, tengan versiones y sean replicables en otros proyectos o entornos de forma idéntica.

## 3. El panel de "Tiro al aire" (Bird's Eye View)
Crea un dashboard que resuma la salud de TODOS tus servicios en una sola pantalla. Si todo está en verde, puedes irte a comer. Si hay un rojo, haces "drill-down" (bajas al detalle) en el dashboard específico de ese servicio.

## 4. Alertas de "Falta de Datos"
En cloud, que algo no DIGA nada es a menudo peor que que diga que hay un ERROR.
*   Asegúrate de tener alertas de "Data Inactivity". Si un proceso de ingesta no ha emitido ningún dato en 4 horas, avísame.

## 5. Centralización de Logs de Error
Usa **Error Reporting**. Es un servicio de GCP que agrupa automáticamente miles de logs de error similares en una sola entrada, te dice cuántas veces ha pasado y te permite marcar el error como "Aceptado", "Arreglado" o "Investigando".

## 6. Seguridad y Auditoría (Cloud Audit Logs)
Activa siempre los logs de auditoría para saber:
*   ¿Quién borró esta tabla de BigQuery?
*   ¿Quién cambió los permisos de este bucket?
Esto no es para castigar, es para entender cambios de configuración accidentales que rompen pipelines.

## Resumen: Profesionalismo en la Nube
La observabilidad en cloud es una disciplina de sistemas tanto como de datos. Aplicar estas buenas prácticas asegura que tu plataforma sea escalable, auditable y, sobre todo, fácil de gestionar por cualquier miembro del equipo.
