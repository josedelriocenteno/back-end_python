# Privacidad y PII: Protegiendo al usuario

PII (Personally Identifiable Information) es cualquier dato que permita identificar a una persona real. Manejarlo mal puede suponer multas millonarias (GDPR).

## 1. Ejemplos de PII
- Nombre completo, DNI, Email, Teléfono.
- Dirección IP, geolocalización exacta.
- Datos de salud o financieros.

## 2. Anonimización vs. Seudonimización
- **Anonimización:** Eliminar el dato para siempre. (Ej: Borrar la columna `email`). Irreversible.
- **Seudonimización:** Cambiar el email por un ID aleatorio (`Hash`). Puedes seguir analizando el comportamiento del usuario sin saber quién es. Reversible si tienes la "llave" del hash.

## 3. Enmascaramiento de Datos (Data Masking)
Consiste en ocultar parte del dato:
- `user_email@gmail.com` -> `u***l@gmail.com`
- Útil para que los desarrolladores puedan testear con datos reales sin ver información privada.

## 4. El "Derecho al Olvido" (Derecho de Supresión)
Bajo el GDPR, si un usuario pide que borres sus datos, debes hacerlo en todos tus sistemas.
- **Reto:** ¿Cómo borras a un usuario de un archivo Parquet de hace 2 años guardado en S3?
- **Solución:** Arquitecturas Lakehouse (Delta/Iceberg) que permiten ejecutar `DELETE` sobre archivos, o guardar el PII en una tabla aparte fácil de borrar.

## 5. Cifrado (Encryption)
- **En reposo (At Rest):** El disco duro de la nube debe estar cifrado por si alguien roba el hardware físico.
- **En tránsito (In Transit):** Toda comunicación debe ir por HTTPS/TLS. Nunca envíes datos sensibles en plano por la red.

## Resumen: Ética y Ley
Nuestra responsabilidad técnica es también una responsabilidad ética. Proteger el PII no es solo cumplir la ley, es respetar la privacidad de las personas que confían en nuestro producto.
