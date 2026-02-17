# Roles Predefinidos: La vía rápida

Google Cloud ofrece cientos de roles listos para usar, agrupados por servicios, para que no tengas que crear configuraciones complejas desde cero.

## 1. Roles Primitivos (Legacy)
Son los roles históricos y **muy peligrosos** porque son demasiado amplios:
- **Owner (Propietario):** Control total, puede borrar el proyecto y gestionar la facturación.
- **Editor:** Puede crear y borrar casi cualquier recurso, pero no puede gestionar permisos de otros.
- **Viewer (Lector):** Solo puede ver la configuración, no puede ver los datos de las tablas ni crear nada.
- **NUNCA** los uses para automatismos ni para dar accesos diarios a desarrolladores. Son demasiado potentes.

## 2. Roles Predefinidos (Recomendados)
Cada servicio tiene sus propios roles específicos. Ejemplos en Data:
- **BigQuery Data Viewer:** Solo puede leer datos de las tablas.
- **BigQuery Job User:** Puede ejecutar queries (pagando por el cómputo).
- **Storage Object Admin:** Puede subir y borrar archivos de un Bucket.
- **Storage Object Viewer:** Solo puede descargar archivos.

## 3. Roles de Administración vs. Usuarios
- **Admin:** Para personas que gestionan el sistema (crear tablas, borrar datasets).
- **User/Viewer:** Para personas o aplicaciones que solo consumen el dato.

## 4. Cómo encontrar el rol adecuado
En la consola de IAM, Google tiene un buscador de roles. Busca siempre el rol que tenga la palabra "Viewer" o "Reader" antes de dar uno que diga "Admin" o "Owner".

## 5. Combinación de Roles
Un usuario puede tener varios roles. Por ejemplo, un analista puede necesitar:
- `BigQuery Data Viewer` (para leer datos).
- `BigQuery Job User` (para poder lanzar la query).
Sin ambos, no podrá trabajar.

## Resumen: Usa lo que ya existe
Los roles predefinidos cubren el 95% de las necesidades de un equipo de datos. Úsalos siempre en lugar de los roles primitivos para mantener un entorno seguro y profesional.
