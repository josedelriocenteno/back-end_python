# Datos Sensibles en la Base de Datos

En la era del RGPD (GDPR) y la privacidad, guardar datos sin control puede llevar a multas astronómicas y pérdida de confianza de los usuarios. Como desarrollador Backend, debes saber qué datos son sensibles y cómo tratarlos.

## 1. Tipos de Datos Sensibles (PII)

*   **PII (Personally Identifiable Information):** Nombres, emails, teléfonos, direcciones.
*   **Credenciales:** Passwords, tokens de API, llaves privadas.
*   **Datos Especiales:** Información médica, religiosa, política u orientación sexual.
*   **Financieros:** Números de tarjeta (PAN), historial de transacciones.

## 2. Reglas de Oro del Almacenamiento

### A. No Guardes lo que no Necesites
La mejor forma de proteger un dato es no tenerlo. Si no necesitas el teléfono del usuario para tu lógica de negocio, no lo pidas ni lo guardes.

### B. Cifrado en Reposo (Encryption at Rest)
El disco duro de tu servidor de DB debe estar cifrado. Si alguien roba físicamente el servidor, no podrá leer los datos.

### C. Hashing para Passwords
**NUNCA** guardes contraseñas en texto plano. Usa algoritmos como `bcrypt`, `Argon2` o `scrypt`.
*   *Postgres Tip:* Usa la extensión `pgcrypto` si necesitas hashear dentro de SQL.

## 3. Técnicas de Protección Avanzada

### Encriptación a nivel de campo (Field Level Encryption)
Para datos extremadamente sensibles (ej: número de seguridad social), se encriptan en el código Python antes de enviarlos a SQL y se desencriptan al leerlos. La base de datos solo ve "ruido".

### Anonimización vs Seudonimización
*   **Anonimización:** Eliminar irreversibilidad el vínculo entre el dato y la persona. (Útil para analítica).
*   **Seudonimización:** Sustituir un identificador real (email) por uno artificial (UUID). Se puede revertir si tienes la "llave".

## 4. Auditoría de Acceso

¿Quién ha consultado los datos de este usuario? 
*   Activa logs de auditoría para ver qué queries de lectura se ejecutan sobre tablas sensibles.
*   PostgreSQL tiene extensiones como `pgaudit` para esto.

## 5. El Derecho al Olvido

Debes tener mecanismos para borrar totalmente a un usuario si lo solicita. Esto incluye:
1.  Borrar su fila en `Users`.
2.  Borrar sus fotos en almacenamiento S3.
3.  Asegurarte de que sus datos desaparezcan de los backups en el tiempo legal establecido (ej: 30 días).

## Resumen: Ética y Legalidad

La seguridad de los datos sensibles no es un "extra", es parte vital del modelado de datos moderno. Diseña tu base de datos pensando en la privacidad desde el primer día (Privacy by Design).
