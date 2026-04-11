# Control de Costes: Budgets y Límites

El Cloud es una tarjeta de crédito sin límite si no tienes cuidado. El control de costes (FinOps) es una parte fundamental del rol de un Data Engineer Senior.

## 1. Configuración de Budgets (Presupuestos)
Define cuánto quieres gastar al mes (ej: 500€).
- Crea alertas al 50%, 90% y 110%.
- **OJO:** Un presupuesto en Google Cloud **NO apaga tus servicios** automáticamente cuando se llega al límite. Solo te avisa.

## 2. Quotas y Límites de Seguridad
Para evitar que un error borre el presupuesto de un mes en una noche, configura límites técnicos:
- Limita el número de CPUs máximas que puede levantar tu equipo.
- Configura en BigQuery el límite de "Bytes facturados por consulta".

## 3. Exportación de Facturación
Activa la exportación de la facturación a BigQuery.
- Google creará una tabla con cada céntimo gastado, desglosado por servicio, por región y por tus etiquetas (Labels).
- **Utilidad:** Puedes crear un dashboard en Looker Studio para que los jefes vean el gasto en tiempo real.

## 4. Etiquetas: La base del control
Si no usas etiquetas (`equipo:data`, `proyecto:ventas`), a final de mes verás una factura de 5.000€ y no sabrás qué parte es de desarrollo y qué parte es de producción.
- Obliga a tu equipo a etiquetar cada recurso que cree.

## 5. El bot de Apagado (Costo $0)
Para entornos de desarrollo:
- Configura una Cloud Function (programada via Cloud Scheduler) que apague todas las máquinas virtuales y bases de datos a las 20:00 y las encienda a las 08:00. Ahorrarás el **60%** del coste de desarrollo.

## Resumen: Responsabilidad Financiera
El éxito de un proyecto cloud no es solo técnico, es económico. Aprender a presupuestar, monitorizar y reaccionar al gasto es lo que genera confianza en el negocio para seguir invirtiendo en la plataforma de datos.
