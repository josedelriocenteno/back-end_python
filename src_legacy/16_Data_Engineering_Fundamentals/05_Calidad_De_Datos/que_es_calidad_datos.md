# ¿Qué es la Calidad de Datos? Por qué es tu prioridad #1

"Garbage In, Garbage Out" (Entra basura, sale basura). No importa lo avanzado que sea tu modelo de IA; si el dato es malo, la decisión de la empresa será errónea.

## 1. Las 6 Dimensiones de la Calidad
Un Data Engineer profesional mide estos 6 puntos para certificar un dataset:
1. **Exactitud (Accuracy):** ¿El dato representa la realidad?
2. **Integridad (Completeness):** ¿Faltan valores críticos (Nulls)?
3. **Consistencia (Consistency):** ¿El dato es el mismo en todos los sistemas?
4. **Validez (Validity):** ¿Cumple con el formato y rango esperado?
5. **Puntualidad (Timeliness):** ¿El dato llega a tiempo para ser útil?
6. **Unicidad (Uniqueness):** ¿Hay registros duplicados?

## 2. El coste de la mala calidad
- **Pérdida de confianza:** Los usuarios dejan de usar tus dashboards si los números no cuadran.
- **Coste Económico:** Mandar una carta a una dirección mal escrita o cobrar de más a un cliente.
- **Riesgo Legal:** Datos sensibles no protegidos o reportes fiscales incorrectos.

## 3. Data Observability
Es la evolución de la monitorización. No solo miramos si el pipeline "corre", miramos si los datos dentro del pipeline "tienen sentido".
- **Herramientas:** Great Expectations, Monte Carlo, Soda.

## 4. Tip Senior: No borres, etiqueta
Si encuentras datos de mala calidad, no los borres sin más. Márcalos con una bandera (ej: `is_valid=False`) y muévelos a una tabla de **"Quarantine"** (Cuarentena). Esto permite investigar la fuente del error sin contaminar la analítica.

## Resumen: Fiabilidad absoluta
Tu trabajo no es solo mover bits; es mover confianza. La calidad de datos es lo que separa a un desarrollador que hace scripts de un Ingeniero de Datos que construye sistemas críticos.
