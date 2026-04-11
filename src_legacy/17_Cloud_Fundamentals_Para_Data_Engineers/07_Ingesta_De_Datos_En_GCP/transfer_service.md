# BigQuery Data Transfer Service (BQ DTS)

A veces, la mejor forma de ingestar datos es no programar nada. Google ofrece el **Data Transfer Service (DTS)** para automatizar la copia de datos desde otras nubes o servicios de Google.

## 1. Fuentes Automáticas
DTS puede traer datos sin código desde:
- **Google Ads:** Carga diaria de tus campañas.
- **YouTube Analytics:** Estadísticas de canales.
- **Amazon S3:** Copia archivos de AWS a GCP.
- **Google Play:** Ventas de apps.

## 2. Ingesta desde otras Bases de Datos
Puedes configurar transferencias desde:
- **Teradata.**
- **Amazon Redshift.**
Permite migrar Data Warehouses enteros de la competencia a BigQuery con un configurador visual.

## 3. Programación y Monitorización
Puedes definir que la transferencia ocurra a una hora concreta del día. DTS se encarga de:
- Gestionar los errores y reintentos.
- Enviarte una alerta si la transferencia falla.
- Mantener el histórico de lo que se ha copiado.

## 4. Ventajas
- **Sin servidores:** No necesitas una Cloud Function ni una VM para que esto corra. Es un servicio gestionado de Google.
- **Seguridad:** Utiliza conexiones nativas y seguras entre nubes.
- **Mantenimiento Cero:** Si Google cambia el formato de los logs de Google Ads, ellos actualizan DTS por ti.

## 5. Cuándo usarlo
- Úsalo siempre para datos de Marketing (Ads, Search Console). Es mucho más fiable que escribir tú el script contra sus complejas APIs.

## Resumen: Automatización sin Código
El Data Transfer Service es el "Fivetran" gratuito de Google Cloud. Permite que el Data Engineer se libere de las tareas de ingesta más repetitivas y se centre en el modelado y la analítica avanzada de los datos recibidos.
