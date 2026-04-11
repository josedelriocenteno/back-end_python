# Cumplimiento Básico (GDPR y Privacidad)

Si tu API maneja datos de ciudadanos de la Unión Europea (o de casi cualquier sitio moderno), debes cumplir con el **GDPR** (Reglamento General de Protección de Datos). No es solo legal, es una cuestión de ética de datos.

## 1. El concepto de PII
**Personally Identifiable Information:** Cualquier dato que permita identificar a una persona.
- **Directo:** Email, Nombre real, DNI.
- **Indirecto:** Dirección IP, Coordenadas GPS, Identificador de dispositivo.

## 2. Los Derechos del Usuario (Capa Backend)
Tu API debe estar preparada para cumplir estos derechos:
- **Derecho al Olvido (Borrado):** Debes poder borrar TODOS los datos de un usuario. ¡Ojo! También de los backups y de los logs (esto último se resuelve anonimizando).
- **Portabilidad de Datos:** Debes ofrecer un endpoint (ej: `GET /me/export`) que devuelva sus datos en un formato estándar (JSON/CSV).
- **Derecho de Acceso:** El usuario debe saber qué datos tienes sobre él.

## 3. Minimización de Datos
**"Si no lo tienes, no lo pueden robar".**
- No pidas la fecha de nacimiento si solo necesitas saber si es mayor de 18.
- No guardes la IP del usuario para siempre si solo la usas para detectar fraude en el login. Borra o anonimiza los datos antiguos que ya no sirven a su propósito original.

## 4. Privacidad por Diseño (Privacy by Design)
- La configuración por defecto debe ser la más restrictiva.
- Los datos sensibles deben estar cifrados por defecto.
- El consentimiento para usar los datos debe ser explícito, no un checkbox marcado por defecto.

## 5. Transferencia Internacional de Datos
Ten cuidado donde guardas los datos. Si usas servidores en EEUU, asegúrate de que el proveedor cumple con los acuerdos de privacidad vigentes (Data Privacy Framework).

## Resumen: El desarrollador como custodio
Un desarrollador backend senior no ve los datos como "bits", los ve como la confianza de los usuarios. Cumplir con GDPR no es rellenar papeles, es diseñar sistemas que respeten la autonomía y la privacidad de las personas.
