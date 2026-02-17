# Seguridad en Datos: Protección de la Joya de la Corona

Una vez que tenemos el IAM configurado, debemos aplicar capas de seguridad adicionales específicas para los datos sensibles.

## 1. Cifrado (Encryption)
- **Por defecto:** Google cifra todos los datos en reposo y en tránsito automáticamente.
- **CMEK (Customer-Managed Encryption Keys):** Si tu empresa es muy estricta, puedes usar tus propias llaves de cifrado gestionadas en **Google Cloud KMS**. Si borras la llave, el dato se vuelve ilegible para siempre, incluso para Google.

## 2. VPC Service Controls (Perímetros de Seguridad)
Imagina que un empleado con permisos legítimos intenta copiar datos de un Bucket de la empresa a su propio Bucket personal de Gmail. 
- Los **VPC Service Controls** crean un muro invisible alrededor de tus servicios de datos para que la información no pueda salir del entorno de la empresa, aunque el usuario tenga permisos de IAM.

## 3. Data Masking y PII
Como vimos en el tema de Data Engineering, GCP ofrece herramientas como **Cloud DLP** (Data Loss Prevention).
- Escanea automáticamente tus tablas de BigQuery buscando emails, números de tarjeta o DNI y los enmascara o cifra automáticamente.

## 4. Acceso Just-in-Time (JIT)
En lugar de que un ingeniero tenga acceso a Producción siempre, el acceso se solicita para una tarea concreta y caduca en 2 o 4 horas. Esto reduce el "tiempo de exposición" en caso de que la cuenta del ingeniero sea hackeada.

## 5. Cloud Audit Logs
Existen tres tipos de logs de auditoría:
- **Admin Activity:** Quién cambió la configuración. (Siempre activados y gratis).
- **Data Access:** Quién leyó la tabla o bajó el archivo. (Debes activarlos manualmente porque generan mucho volumen y coste). **Obligatorio en entornos regulados**.
- **System Event:** Acciones automáticas del sistema Google.

## Resumen: Defensa en Profundidad
La seguridad no es una puerta con llave, es una cebolla con muchas capas. IAM es la primera, el cifrado la segunda, el perímetro de red la tercera y la auditoría la última. Un Data Engineer Senior diseña sistemas que resisten fallos en cualquiera de estas capas.
