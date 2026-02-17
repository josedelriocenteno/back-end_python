# Autenticación desde Python: ADC es la clave

El mayor quebradero de cabeza al empezar con la nube es: "¿Cómo sabe mi código que soy yo y que tengo permisos?". Google resuelve esto con **ADC (Application Default Credentials)**.

## 1. ¿Cómo funciona ADC?
Es una estrategia de búsqueda de credenciales. Cuando haces `storage.Client()`, la librería busca en este orden:
1. Una variable de entorno llamada `GOOGLE_APPLICATION_CREDENTIALS` que apunte a un JSON.
2. Si corres en GCP (VM, Cloud Run, Function), Google usa la identidad de la **Service Account** asociada automáticamente.
3. Si estás en local, busca las credenciales guardadas por el comando `gcloud auth application-default login`.

## 2. Autenticación en Local (Desarrollo)
Para que tus scripts de Python conecten a GCP desde tu ordenador:
```bash
gcloud auth application-default login
```
Esto abrirá tu navegador, inicias sesión con tu cuenta de empresa, y listo. Tu código Python ahora usará tus permisos de usuario de GCP.

## 3. Autenticación en Producción (Cloud)
**NUNCA** uses archivos JSON dentro de tus servicios en la nube. 
- Asocia una Service Account al servicio (ej: Cloud Run).
- Dale los permisos necesarios en la consola de IAM.
- Tu código detectará la identidad **sin necesidad de archivos de claves ni passwords**. Es la forma más segura del mundo.

## 4. El peligro de las Hardcoded Keys
Nunca hagas esto: `client = storage.Client.from_service_account_json('llave.json')`.
- Si ese archivo acaba en Git, tu nube está en peligro.
- Si usas ADC, el código es el mismo para local y para producción, lo que facilita el testing.

## 5. Resumiendo el Checklist de Seguridad
- Local -> `gcloud auth application-default login`.
- Producción -> Asignar Service Account al recurso de cómputo.
- Olvida los archivos JSON siempre que sea posible.

## Resumen: Transparencia y Seguridad
ADC es lo que permite que el mismo código Python funcione en tu portátil y en un servidor con miles de núcleos en la nube de forma transparente. Entender este flujo es vital para evitar problemas de permisos y brechas de seguridad.
