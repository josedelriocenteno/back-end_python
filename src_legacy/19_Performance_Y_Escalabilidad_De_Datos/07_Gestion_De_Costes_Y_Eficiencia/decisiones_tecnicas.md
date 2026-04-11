# Decisiones Técnicas y su Impacto Económico

Toda decisión de arquitectura tiene una cara B: la factura a final de mes. Aprende a evaluar el coste antes de escribir la primera línea de código.

## 1. Base de Datos: ¿Relacional o NoSQL?
*   **Relacional (Postgres):** Coste fijo mensual por servidor. Predecible.
*   **NoSQL Serverless (Firestore/DynamoDB):** Pagas por cada lectura/escritura. Barato si tienes poco tráfico, pero puede volverse carísimo si tu App se vuelve muy activa.

## 2. Formato de Archivos: ¿CSV o Parquet?
*   **CSV:** Fácil de leer para humanos. Gigante en disco. Lentísimo de escanear en BigQuery (pagas más).
*   **Parquet:** Comprimido. Binario. BigQuery solo lee las columnas necesarias (pagas muchísimo menos). No hay excusa para usar CSV en un Data Lake de producción.

## 3. Logs: ¿INFO o DEBUG?
*   Loguear cada detalle puede generar Terabytes de datos. Google Cloud Logging cobra por GB.
*   **Consecuencia:** Un error en tu configuración de logs puede costar más que el propio servidor que los genera.

## 4. Retención de Backups
*   ¿Necesitas backups diarios de los últimos 10 años? El almacenamiento Archive es barato, pero 3.650 backups NO lo son.
*   **Decisión:** Define una política de retención sensata (ej: diarios 30 días, mensuales 1 año, anuales 5 años).

## 5. Multinube (Multi-cloud) vs Proveedor Único
*   **Proveedor Único:** Descuentos mejores por volumen. Menos costes de mover datos (egress).
*   **Multinube:** Evitas el "Vendor Lock-in", pero pagas fortunas en mover datos entre Google y AWS. No lo hagas a menos que sea una necesidad crítica de negocio.

## Resumen: La Arquitectura Cuesta Dinero
Como Data Engineer, tus decisiones técnicas pesan en el balance de resultados de la empresa. Elegir el formato, la base de datos y la política de retención adecuada es lo que diferencia a un programador de un Arquitecto de Datos eficiente y profesional.
