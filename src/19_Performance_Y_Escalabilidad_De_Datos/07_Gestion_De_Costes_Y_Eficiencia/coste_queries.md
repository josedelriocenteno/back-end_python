# El Coste de las Consultas: BigQuery y SQL Eficiente

En bases de datos modernas como **BigQuery** o **Snowflake**, no pagas por tener la base de datos encendida, pagas por cada consulta que lanzas según la cantidad de datos que escanea.

## 1. El peligro del "SELECT *"
En BigQuery, si una tabla tiene 100 columnas y 1TB de datos, y tú haces `SELECT * LIMIT 10`:
*   **Pagas por el escaneo del 1TB completo**, aunque solo pidas 10 filas.
*   **Solución:** Selecciona solo las columnas necesarias: `SELECT id, nombre...`. BigQuery es una base de datos **columnar** y solo te cobrará por las columnas que toques.

## 2. Particionado y Clustering: Ahorro Masivo
Como vimos en sub-módulos anteriores, estas técnicas físicas impactan directamente en el bolsillo:
*   **Particionado:** Si filtras por fecha y la tabla está particionada, BigQuery solo escanea el trozo de datos de ese día. La factura baja un 99%.
*   **Clustering:** Ordena los datos físicamente para que el motor encuentre los valores más rápido gastando menos recursos.

## 3. Vistas Materializadas y Caché
*   **Vistas Materializadas:** Pre-calculan el resultado y lo guardan. Consultar una vista materializada es mucho más barato que ejecutar la query compleja cada vez.
*   **Caché de Resultados:** BigQuery no te cobra si lanzas la misma query exacta que alguien lanzó hace 5 minutos (y los datos no han cambiado).

## 4. Reserva de Slots (Slots Reservation)
Si tu empresa lanza MILES de queries al día, el modelo de pago por consulta (On-demand) puede ser impredecible y caro.
*   **Solución:** "Alquila" una cantidad fija de potencia de cálculo mensual (**Slots**). El precio es fijo y puedes lanzar todas las queries que quieras dentro de ese margen.

## 5. Límites de Facturación (Quotas)
No querrás que una query mal escrita por un error de un desarrollador cueste 1.000$.
*   Configura límites a nivel de proyecto o usuario para que ninguna consulta individual pueda escanear más de X Gigabytes.

## Resumen: Consultas de Precisión
En el mundo del Data Warehouse moderno, cada punto y coma cuenta. Escribir SQL eficiente no es solo una cuestión técnica; es una responsabilidad presupuestaria. Entiende cómo cobra tu proveedor y diseña tus tablas y consultas para minimizar el escaneo de datos innecesarios.
