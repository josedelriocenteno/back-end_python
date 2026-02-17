# Normalización vs. Desnormalización

El diseño de una base de datos es un equilibrio constante entre el ahorro de espacio y la velocidad de lectura. Estas son las dos estrategias principales.

## 1. Normalización (3NF)
Divide los datos en muchas tablas relacionadas para evitar la duplicidad.
*   **Objetivo:** Integridad de los datos. Si un cliente cambia de dirección, solo lo cambias en un sitio.
*   **Pros:** Menos uso de disco, actualizaciones rápidas y consistentes. No hay anomalías de inserción.
*   **Contras:** Consultar los datos requiere muchos `JOINS`, lo que ralentiza las lecturas.
*   **Uso:** Sistemas transaccionales (OLTP), como el backend de una tienda online.

## 2. Desnormalización
Duplica datos a propósito en una misma tabla para evitar uniones.
*   **Objetivo:** Velocidad de lectura extrema.
*   **Pros:** Consultas muy simples y rápidas (sin Joins). Ideal para grandes volúmenes.
*   **Contras:** Más uso de disco, riesgo de inconsistencia (si cambias un dato en un sitio, tienes que acordarte de cambiarlo en todos los duplicados).
*   **Uso:** Sistemas analíticos (OLAP), Data Warehouses y Dashboards de BI.

## 3. El Trade-off (Compromiso)
Como Data Engineer, te moverás entre ambos mundos:
- Los datos te llegarán **normalizados** desde las aplicaciones de negocio.
- Tú los transformarás y los **desnormalizarás** para que los analistas puedan consultarlos rápido.

## 4. Técnicas de Desnormalización Táctica
*   **Añadir columnas de referencia:** Poner el `nombre_producto` directamente en la tabla de `ventas`.
*   **Tablas de Agregados:** Pre-calcular la suma de ventas diaria y guardarla en una tabla en lugar de calcularla cada vez que alguien abre un informe.
*   **Campos JSON:** Guardar datos secundarios menos importantes en un campo `JSONB` en lugar de una tabla de 1:N separada.

## 5. Cuándo desnormalizar
1. Cuando un `JOIN` entre tablas gigantes es el cuello de botella.
2. Cuando la tabla de origen casi nunca cambia (datos históricos).
3. Cuando necesitas dar servicio a una API de baja latencia.

## Resumen: Elige tu batalla
No existe el modelo perfecto "por defecto". Normaliza para escribir datos con seguridad; desnormaliza para leer datos con velocidad. Un ingeniero senior sabe cuándo romper las reglas de la normalización en favor del rendimiento del negocio.
