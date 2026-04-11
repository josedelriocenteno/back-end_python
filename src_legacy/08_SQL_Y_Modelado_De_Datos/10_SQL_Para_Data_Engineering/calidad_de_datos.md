# Calidad de Datos: Tu Última Línea de Defensa

En un pipeline de Data Engineering, "Basura entra, Basura sale" (GIGO - Garbage In, Garbage Out). La calidad de los datos no es opcional; es una responsabilidad del ingeniero.

## 1. Los 5 Pilares de la Calidad de Datos

1.  **Integridad:** ¿Están todos los datos necesarios? (Evitar nulos inesperados).
2.  **Unicidad:** ¿Hay duplicados? (Control de claves primarias).
3.  **Consistencia:** ¿El dato significa lo mismo en todas las tablas? (Referencial).
4.  **Validez:** ¿El dato sigue el formato esperado? (Estructura y tipos).
5.  **Actualidad:** ¿Los datos están al día? (Frescura/Timeliness).

## 2. Validaciones Proactivas con SQL

Usa SQL para detectar problemas antes de que lleguen a tus dashboards o modelos de ML.

### Detección de Nulos Críticos:
```sql
SELECT count(*) 
FROM sales_staging 
WHERE customer_id IS NULL OR amount <= 0;
```

### Comprobación de Rango y Lógica:
```sql
SELECT * FROM health_records
WHERE heart_rate < 30 OR heart_rate > 220;
```

### Consistencia de Relaciones (Orphans):
Para detectar registros que no tienen un padre correspondiente (si no podías usar FK por ser tablas de diferentes orígenes).
```sql
SELECT s.order_id
FROM sales_staging s
LEFT JOIN users u ON s.user_id = u.id
WHERE u.id IS NULL;
```

## 3. Pruebas Automatizadas (Data Contracts)

Herramientas como **dbt (data build tool)** o **Great Expectations** te permiten definir estas reglas como "Tests". 
*   Si una query de validación devuelve filas, la carga falla y se detiene el pipeline.

## 4. Gestión de Datos Corruptos: El "Quarantine Pattern"

En lugar de que todo el proceso falle por una sola fila mal formada:
1.  **Valida:** Identifica las filas que fallan.
2.  **Aísla:** Mueve esas filas a una tabla de "Cuarentena" (`quarantine_table`).
3.  **Procesa el resto:** Continúa con los datos sanos.
4.  **Notifica:** Lanza una alerta (Slack/Email) con los IDs corruptos para revisión manual.

## 5. Auditoría de Calidad

Es una buena práctica tener una tabla de `data_quality_logs` que guarde métricas de cada carga:
*   Fecha de carga.
*   Total de filas procesadas.
*   Total de filas rechazadas.
*   Motivo del rechazo.

## Resumen: Confía pero Verifica

No asumas que el origen de datos siempre enviará la información correcta. Tu trabajo como ingeniero es construir "puertas de calidad" en cada etapa de tu pipeline de SQL.
