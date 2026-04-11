# Git en Data Engineering: Versionado de Pipelines

En Ingeniería de Datos, el reto no es solo el código, sino el flujo del dato y la infraestructura.

## 1. SQL Versionado
Evita tener scripts SQL sueltos. Todo el DDL (Data Definition Language) debe estar en archivos `.sql` en Git.
- Usa herramientas como **dbt (data build tool)** para que el SQL sea modular y versionable.

## 2. Definición de Infraestructura (IaC)
Tus pipelines (Airflow DAGs) o la creación de buckets en la nube deben estar en Git (Terraform / CloudFormation).
- Si no está en Git, la infraestructura no existe.

## 3. El problema de los Notebooks (`.ipynb`)
Los Jupyter Notebooks son archivos JSON gigantes que guardan el output (gráficas, datos). Hacer un `diff` de un notebook en Git es una pesadilla.
- **Solución:** Limpia los outputs antes de commitear o usa extensiones como **nbstripout** para que Git solo guarde el código, no las imágenes generadas.

## 4. Orquestación de Cambios
Cuando cambias un pipeline, no puedes simplemente hacer "push". Debes asegurar que los datos antiguos siguen siendo compatibles o ejecutar un proceso de "Backfill" (re-procesar datos pasados). Documenta este proceso en la Pull Request.

## 5. Branching para entornos de datos
- `main`: Datos de producción.
- `staging`: Datos de prueba/validación.
- Los DAGs de Airflow deben leer su configuración de ramas diferentes para apuntar a buckets de datos diferentes.

## Resumen: Integridad del Dato
Data Engineering usa Git para asegurar que el "camino" que sigue el dato es reproducible y que cualquier cambio en la tubería está auditado.
