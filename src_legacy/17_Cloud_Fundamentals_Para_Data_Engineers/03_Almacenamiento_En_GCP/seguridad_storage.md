# Seguridad en Cloud Storage: Permisos y Acceso

Proteger los archivos en GCS es fundamental, ya que ahí reside el Big Data de la compañía. Tenemos tres niveles de control.

## 1. IAM a nivel de Bucket (Recomendado)
Es la forma moderna y escalable. Das permiso a un usuario o grupo sobre todo el Bucket.
- **Roles:** `Storage Object Viewer` (Leer), `Storage Object Creator` (Subir), `Storage Admin` (Control total).
- **Uniform Bucket-level Access:** Activa siempre esta opción. Evita el caos de tener permisos diferentes en cada archivo individual.

## 2. ACLs (Access Control Lists) - Antigua
Permite dar permisos archivo por archivo (ej: "Juan puede ver `foto1.jpg` pero no `foto2.jpg`").
- **Tip Senior:** Evita las ACLs siempre que puedas. Son difíciles de auditar y gestionar a escala de millones de archivos.

## 3. Signed URLs (URLs Firmadas)
¿Quieres que un usuario que NO tiene cuenta de Google pueda descargar un archivo específico durante los próximos 10 minutos?
- Generas una **Signed URL**. Es un enlace temporal con una firma criptográfica que caduca automáticamente. 
- Muy útil para que tu App de Backend le dé acceso a un usuario a su factura PDF sin hacer público el bucket.

## 4. Buckets Públicos (Peligro)
Nunca hagas un bucket público a menos que contenga activos de una web (imágenes, CSS). 
- Google te avisará con una alerta roja gigante. Un bucket público mal configurado es la causa número 1 de robo de datos en la nube.

## 5. Encriptación
Como vimos en seguridad, puedes usar:
- **Google Managed Keys:** (Por defecto, automático).
- **CSEK (Customer-Supplied Encryption Keys):** Tú envías la llave en cada petición. Si la pierdes, Google NO puede recuperar tus datos.

## Resumen: Acceso Privado por Defecto
En Cloud Storage, la regla es: Todo es privado hasta que tú digas lo contrario. Usa IAM para usuarios de la empresa y Signed URLs para usuarios externos, manteniendo siempre el control total de quién ve tus datos.
