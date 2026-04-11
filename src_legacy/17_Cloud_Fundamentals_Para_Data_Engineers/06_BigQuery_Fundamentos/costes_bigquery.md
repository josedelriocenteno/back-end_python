# Costes en BigQuery: Entendiendo la factura

BigQuery es barato si sabes usarlo, pero puede ser carísimo si lanzas queries mal optimizadas. Hay dos componentes principales en el coste.

## 1. Coste de Almacenamiento (Storage)
Lo que pagas por tener el dato guardado en los discos de Google.
- **Active Storage:** Datos que has modificado en los últimos 90 días.
- **Long-term Storage:** Si no tocas una partición/tabla en 90 días, el precio baja un **50%** automáticamente.
- **Tip:** BigQuery es una forma muy barata de guardar datos históricos, compitiendo incluso con Cloud Storage.

## 2. Coste de Análisis (Compute)
Lo que pagas por procesar los datos con queries. Hay dos modelos:
- **On-Demand (Pago por uso):** Pagas una tarifa fija (ej: 5€) por cada Terabyte leído. Ideal para equipos pequeños o cargas variables.
- **Capacity (Reservation):** Pagas por "Slots" (unidades de potencia de CPU) de forma mensual o anual. Ideal para grandes empresas que quieren una factura fija y predecible.

## 3. Operaciones GRATUITAS
Aprovecha estas operaciones para ahorrar:
- Cargar datos desde Cloud Storage.
- Copiar tablas.
- Exportar datos de BigQuery a Cloud Storage.
- Borrar tablas o datasets.
- Queries sobre metadatos (ej: `__TABLES_SUMMARY__`).

## 4. La barra de "Bytes a procesar"
Antes de darle al botón de "Run" en la consola, fíjate arriba a la derecha. BigQuery te dirá: "This query will process 1.5 GB". Úsalo para estimar el coste antes de ejecutar una query de un Terabyte por error.

## 5. Límites y Controles (Quotas)
Configura límites de gasto a nivel de proyecto o usuario. Puedes decir: "Ningún usuario puede gastar más de 10€ al día en este proyecto". Es el seguro de vida contra el "Becario que lanzó un SELECT * de 100 Terabytes".

## Resumen: Eficiencia Financiera
El coste de BigQuery es tu responsabilidad. Usa particionado, limita los slots y revisa el almacenamiento a largo plazo. Un pipeline que escala técnicamente pero arruina a la empresa no es un buen pipeline.
