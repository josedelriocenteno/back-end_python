# Datos Corruptos: Detección y Drenaje

Por muy buenas que sean tus validaciones, los datos corruptos (malformados o con lógica rota) acabarán llegando. Necesitas un plan de respuesta.

## 1. ¿Cómo se originan?
- Errores de codificación (caracteres extraños, emojis no soportados).
- Fallos en la serialización del sistema origen.
- Truncamiento (un campo de texto de 500 caracteres que se corta a los 50).

## 2. Técnicas de Detección
- **Profilers:** Herramientas que analizan la distribución de los datos (promedio, desviación estándar). Si el promedio de ventas suele ser 50€ y hoy es 5.000€, algo está corrupto.
- **Schema Enforcement:** Configurar el Data Warehouse para que rechace cualquier carga que no cumpla el esquema al 100%.

## 3. El patrón del "Dead Letter Queue" (DLQ)
Copiado de la arquitectura de mensajes.
1. El pipeline intenta procesar el dato.
2. Si el dato es corrupto o falla la validación, se captura la excepción.
3. El dato "malo" se envía a una tabla o carpeta aparte con el motivo del fallo.
4. El pipeline sigue con el siguiente registro.

## 4. Limpieza (Data Scrubbing)
Procesos automatizados que buscan y corrigen errores comunes en reposo:
- Quitar espacios en blanco al principio y final (`trim`).
- Convertir formatos de fecha ambiguos (`01/02` -> ¿Enero 2 o Febrero 1?).

## 5. El peligro de la "Curación Manual"
Evita arreglar datos corruptos a mano en la base de datos de producción. Si lo haces, el error volverá a ocurrir mañana. Arregla la **lógica del pipeline** para que sepa manejar ese caso automáticamente.

## Resumen: Limpieza Sistémica
Un Data Engineer profesional no se queja de los datos corruptos; diseña sistemas que los detectan, los aislan y facilitan su corrección sin detener la operación del negocio.
