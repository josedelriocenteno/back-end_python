# Latencia vs. Coste: El gran compromiso (Trade-off)

En ingeniería de datos, no existe la "mejor" solución, existe la solución que el negocio puede pagar y que cumple los requisitos.

## 1. La Curva del Coste
Casi siempre, reducir la latencia (que el dato llegue antes) aumenta el coste de forma exponencial, no lineal.
- Un proceso diario cuesta **X**.
- Un proceso cada hora cuesta **2X**.
- Un proceso en tiempo real (streaming) puede costar **10X** o más.

## 2. Por qué el Streaming es más caro
1. **Infraestructura Siempre Encendida:** En batch, las máquinas se apagan al terminar. En streaming, los servidores consumen luz y dinero 24/7.
2. **Sistemas Complejos:** Kafka, Flink y clústeres de alta disponibilidad requieren más mantenimiento y personal especializado.
3. **Overhead de Red:** Enviar millones de mensajes pequeños genera más tráfico que un solo archivo comprimido gigante.

## 3. La Regla del Negocio
Antes de elegir, pregunta: "¿Qué pasa si este dato llega 1 hora tarde?".
- Si la respuesta es "La empresa pierde dinero" -> **Streaming**.
- Si la respuesta es "El reporte para el jefe de mañana estará igual de bien" -> **Batch**.

## 4. Optimización de Costes
- Usa **Spot Instances** (servidores más baratos que pueden apagarse) para procesos batch que no sean críticos.
- Agrupa eventos en streaming antes de escribirlos en disco (Buffer) para reducir el coste de I/O.

## Resumen: Sé un Consultor
Tu trabajo no es usar la tecnología más moderna porque sí, sino aconsejar la que mejor se adapte al presupuesto y a la necesidad real del usuario final.
