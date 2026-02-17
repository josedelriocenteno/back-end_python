# Service Accounts: Identidades para Máquinas

Las **Service Accounts** (Cuentas de Servicio) son identidades especiales que no pertenecen a una persona, sino a una aplicación, un script o un servicio de GCP.

## 1. ¿Por qué son vitales?
Tus pipelines de Python, tus funciones Cloud y tus procesos de Airflow necesitan permisos para leer y escribir datos. No puedes usar tu usuario `tu-nombre@empresa.com` porque:
- Tu contraseña caduca.
- Tienes permisos demasiado amplios.
- Si te vas de la empresa, el pipeline se rompería.

## 2. Anatomía de una Service Account
- Tienen un formato de email: `[nombre]@[id-proyecto].iam.gserviceaccount.com`.
- No tienen contraseña. Usan **Claves Criptográficas (Keys)** o **Asociación Directa**.

## 3. Tipos de Autenticación
- **Keys (Archivos JSON):** Bajas un archivo con una clave privada. **PELIGRO:** Si pierdes este archivo o lo subes a GitHub, cualquiera puede entrar en tu nube. Úsalo solo cuando conectes desde fuera de GCP (ej: desde tu ordenador local).
- **Identity Association:** Si tu código corre DENTRO de GCP (ej: en una Cloud Function), no necesitas archivos JSON. Google asocia la identidad automáticamente. Es mucho más seguro.

## 4. Buenas Prácticas con Service Accounts
1. **Una SA por servicio:** No uses la misma SA para el pipeline de Ventas y el de Recursos Humanos.
2. **Nombre Descriptivo:** `sa-ingesta-ventas-prod`.
3. **No subas Keys a Git:** Usa herramientas de gestión de secretos como **Google Secret Manager**.
4. **Rotación de Claves:** Cambia las claves JSON periódicamente.

## 5. El "Service Account Actor"
Es un permiso especial. Permite que un usuario humano "se convierta" en la Service Account para debuguear. Úsalo con cuidado.

## Resumen: Automatización Segura
Las Service Accounts son el motor de la automatización en GCP. Configurarlas correctamente, con los permisos mínimos y sin exponer sus claves, es la tarea más repetitiva e importante de un Data Engineer.
