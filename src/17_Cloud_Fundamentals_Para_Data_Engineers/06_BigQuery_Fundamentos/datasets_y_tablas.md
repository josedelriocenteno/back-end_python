# Datasets y Tablas: Organización en BigQuery

La jerarquía en BigQuery es sencilla pero estricta. Entenderla es vital para gestionar permisos y organizar el trabajo de diferentes equipos.

## 1. La Jerarquía
1. **Proyecto:** (Contenedor de seguridad y facturación).
2. **Dataset:** (Equivalente a una Base de Datos en SQL tradicional). Es donde se definen los permisos y la ubicación geográfica (región).
3. **Tablas / Vistas:** Los objetos que contienen el dato o la lógica.

## 2. Tipos de Tablas
- **Tablas Nativas:** El dato vive dentro de BigQuery. Máximo rendimiento.
- **Tablas Externas:** El dato vive en un Bucket de Cloud Storage (ej: archivos Parquet). Útil para consultar el Data Lake sin mover el dato, pero más lento que las nativas.
- **Vistas:** Queries guardadas. No ocupan espacio.
- **Vistas Materializadas:** El resultado de la query se guarda en disco y se actualiza solo. Combina la velocidad de una tabla con la frescura de una vista.

## 3. Esquemas (Schemas)
Cada tabla tiene un esquema definido (nombre de columna, tipo, modo).
- **Tipos comunes:** `STRING`, `INT64`, `FLOAT64`, `BOOLEAN`, `DATE`, `TIMESTAMP`.
- **Modos:** `REQUIRED` (No nulo), `NULLABLE` (Puede ser nulo), `REPEATED` (Para listas/arrays).

## 4. Organización por Entorno
Un Data Engineer profesional nunca mezcla tablas.
- `mi-proyecto.raw_dataset` (Carga inicial).
- `mi-proyecto.silver_dataset` (Limpio).
- `mi-proyecto.gold_dataset` (Negocio).

## 5. Expiración de Datasets y Tablas
Puedes configurar que una tabla se borre sola pasados X días. Ideal para tablas temporales de staging o datasets de prueba de desarrolladores para que no ocupen espacio y dinero eternamente.

## Resumen: Orden Estructural
Estructura tus datasets por capas de transformación y por dominios de negocio (Ventas, Marketing, Finanzas). Esto facilitará el control de accesos vía IAM y hará que tus analistas encuentren el dato mucho más rápido.
