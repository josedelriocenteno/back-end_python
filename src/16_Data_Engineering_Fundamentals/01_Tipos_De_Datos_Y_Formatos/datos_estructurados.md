# Datos Estructurados: El mundo de las tablas

Los datos estructurados son el tipo de dato más tradicional y fácil de procesar. Siguen un esquema rígido y predefinido.

## 1. Características Principales
- **Esquema Exacto:** Sabes de antemano qué columnas hay, de qué tipo son (Int, String, Date) y si pueden ser nulas.
- **Relacionales:** Se almacenan en tablas conectadas entre sí mediante claves (Foreign Keys).
- **Eficiencia SQL:** Las bases de datos pueden optimizar las búsquedas de forma extrema gracias a los índices.

## 2. Dónde viven: OLTP y OLAP
- **OLTP (Sistemas transaccionales):** PostgreSQL, MySQL. Guardan el día a día de la empresa.
- **OLAP (Sistemas analíticos):** BigQuery, Snowflake. Guardan el historial masivo para reportes.

## 3. Ventajas para el Ingeniero de Datos
- **Calidad Garantizada:** Es difícil insertar basura si la base de datos obliga a cumplir el tipo de datos.
- **Compresión:** Al saber que una columna es solo de números, el sistema puede comprimirla mucho mejor que un texto libre.

## 4. El coste de la rigidez
Cambiar la estructura de un dato estructurado (ej: añadir una columna a una tabla de 1.000 millones de filas) puede ser una operación lenta y peligrosa que requiere migraciones coordinadas.

## Resumen: La base de la analítica
Aunque existan formatos modernos, el destino final del 90% de los datos en una empresa es acabar estructurados en una tabla. Dominar el modelado relacional es la habilidad más rentable para cualquier ingeniero de datos.
