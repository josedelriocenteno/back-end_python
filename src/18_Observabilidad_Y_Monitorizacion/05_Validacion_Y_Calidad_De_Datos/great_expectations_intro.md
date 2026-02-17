# Great Expectations: El estándar de validación

Escribir validaciones manuales en Python está bien para scripts pequeños, pero para proyectos reales usamos frameworks. **Great Expectations (GX)** es la herramienta líder para validar, documentar y monitorizar la calidad de los datos.

## 1. El concepto de "Expectation"
Una "Expectativa" es una afirmación sobre tus datos expresada en un lenguaje amigable.
*   `expect_column_values_to_not_be_null("id_usuario")`
*   `expect_column_values_to_be_between("edad", 0, 120)`
*   `expect_table_row_count_to_be_between(1000, 5000)`

## 2. Ventajas de usar GX
*   **Documentación automática:** GX genera una web (Data Docs) donde cualquiera puede ver qué reglas se están aplicando y si se cumplen.
*   **Independencia del motor:** Puedes validar datos en archivos CSV, en Pandas, en Spark o directamente en bases de datos SQL (Postgres, BigQuery).
*   **Integración:** Se lleva muy bien con Airflow, Prefect y dbt.

## 3. Flujo de trabajo con GX
1.  **Connect:** Conectas GX a tu fuente de datos.
2.  **Create:** Defines tus expectativas (puedes hacerlo interactivamente).
3.  **Validate:** Corres el "Checkpoint" contra tus datos nuevos.
4.  **Review:** Miras los resultados en los Data Docs y lanzas alertas si algo falla.

## 4. Ejemplo rápido (Conceptual)
```python
import great_expectations as gx

# 1. Obtener el contexto y el batch de datos
context = gx.get_context()
validator = context.get_validator(datasource_name="my_db", data_asset_name="users")

# 2. Definir expectativas
validator.expect_column_values_to_be_unique("email")
validator.expect_column_mean_to_be_between("puntuacion", 1, 10)

# 3. Validar
results = validator.validate()
print(f"¿Los datos son válidos?: {results.success}")
```

## 5. El valor de la "Cerca de Seguridad"
Usar Great Expectations es como poner una valla de seguridad alrededor de tu Data Warehouse. Si un dato intenta entrar y no cumple las normas, GX lo detiene, lo documenta y te avisa, protegiendo todo el ecosistema de datos de la empresa.

## Resumen: Profesionalizando la Calidad
GX transforma la validación de una tarea tediosa de programación en un proceso estructurado, documentado y compartible con el resto de la organización. Es la herramienta que separa a los equipos de datos reactivos de los proactivos.
