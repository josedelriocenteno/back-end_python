# Fuentes de Datos: ¿De dónde viene la información?

El primer paso de cualquier pipeline es conectarse a la fuente. Como Data Engineer, debes saber hablar el "idioma" de cada sistema origen.

## 1. Bases de Datos (OLTP)
Las bases de datos que alimentan la aplicación (PostgreSQL, MySQL, MongoDB).
- **Cómo extraer:** Consultas SQL directas o, mejor aún, leyendo el log de transacciones (CDC).
- **Reto:** No sobrecargar la base de datos de producción con consultas pesadas. Usa réplicas de lectura.

## 2. APIs de Terceros
SaaS como Salesforce, Stripe, Shopify, Google Ads.
- **Cómo extraer:** Peticiones HTTP (REST/GraphQL).
- **Reto:** Manejo de autenticación (OAUTH2), límites de velocidad (Rate Limits) y paginación.

## 3. Almacenamiento de Archivos (Object Storage)
Archivos subidos a S3, GCS o carpetas FTP por otros sistemas.
- **Cómo extraer:** Listado y descarga de archivos.
- **Reto:** Gestionar archivos corruptos o subidos a medias.

## 4. Colas de Mensajes y Eventos
Kafka, RabbitMQ, PubSub.
- **Cómo extraer:** Suscripción al tópico y procesamiento en streaming.
- **Reto:** Manejar el orden de los eventos y la persistencia.

## 5. Web Scraping (Casos raros)
Extraer datos directamente de una web que no tiene API.
- **Reto:** Es extremadamente frágil. Si la web cambia un botón, el pipeline se rompe. Úsalo solo como último recurso.

## Resumen: Diversidad Conectada
Un buen ecosistema de datos ingiere de múltiples fuentes. Tu misión es homogeneizar todas estas entradas para que el resto del sistema las vea como un flujo de datos limpio y unificado.
