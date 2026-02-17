# Cifrado de Datos Sensibles (At Rest)

Incluso si tu aplicación es perfecta, puede haber un fallo de seguridad en el propio proveedor de Cloud o alguien podría robar los discos duros del servidor. Por eso, los datos deben estar cifrados en reposo.

## 1. ¿Qué debemos cifrar?
No cifres toditito (por rendimiento), pero sí los datos PII (Personally Identifiable Information) críticos:
- Números de cuenta bancaria e IBAN.
- Direcciones físicas exactas.
- Números de identificación oficial (DNI, Pasaporte).
- Historiales médicos o secretos comerciales.
- **Nota:** Las contraseñas NO se cifran, se HASHEAN (revisa el tema 11-02).

## 2. Niveles de Cifrado

### A. Cifrado a nivel de Disco (TDE - Transparent Data Encryption)
- Lo gestiona el proveedor cloud (AWS/GCP/Azure). Todo lo que se escribe en el hardware se cifra automáticamente.
- **Protege contra:** Robo físico de los discos.
- **Fallo:** Si alguien entra en tu servidor encendido, verá los datos en claro porque el disco se descifra al montarse.

### B. Cifrado a nivel de Base de Datos
- Usar funciones propias de la DB (como `pgcrypto` en Postgres).
- El dato viaja cifrado hasta la DB y se guarda cifrado en las tablas.
- **Protege contra:** Alguien que logre hacer un `SELECT *` pero no tenga la llave de pgcrypto.

### C. Cifrado a nivel de Aplicación (El más seguro)
- Tu código Python cifra el dato antes de enviarlo a la DB.
- Usamos librerías como `Cryptography` (AES-256).
- **Protege contra:** Todo lo anterior y también si el administrador de la base de datos intenta cotillear los datos. El DBA verá solo "basura" ilegible.

## 3. Gestión de Claves (KMS)
El mayor problema del cifrado no es el algoritmo (AES-256 es irrompible hoy en día), es dónde guardas la llave.
- **NUNCA:** Guardar la llave de cifrado en la misma base de datos que los datos cifrados.
- **SIEMPRE:** Usar un servicio especializado (AWS KMS, Google KMS) que guarde la llave en hardware seguro (HSM) y controle quién puede usarla.

## 4. Búsquedas en Datos Cifrados
Cifrar un campo lo hace "ciego". Ya no puedes hacer `WHERE email LIKE '%gmail%'` porque el email cifrado es aleatorio.
- **Solución:** Guardar un "Ciego de Búsqueda" (Blind Index), que es un hash del dato original que permite búsquedas exactas pero no revela el contenido real.

## Resumen: Capas de Cebolla
El cifrado en reposo es la última capa de cebolla. Es lo que garantiza que, aunque el desastre ocurra y tus datos sean robados, el atacante se lleve una montaña de bits inservibles.
