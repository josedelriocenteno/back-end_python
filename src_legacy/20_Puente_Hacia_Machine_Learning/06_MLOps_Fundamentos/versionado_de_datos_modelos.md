# Versionado de Datos y Modelos

En el software tradicional, Git es suficiente para versionar el código. En Machine Learning, **Git no es suficiente**, porque el comportamiento del sistema depende también de los Gigabytes de datos y de los archivos binarios del modelo.

## 1. ¿Por qué no usar Git para datos?
*   **Tamaño:** Git se vuelve lento y pesado con archivos de más de unos pocos megas.
*   **Naturaleza:** Git está diseñado para texto (diffs), no para binarios como imágenes o bases de datos SQLite.

## 2. Versionado de Datos (DVC - Data Version Control)
**DVC** es la herramienta estándar que actúa como "el Git de los datos".
*   **Cómo funciona:** Los datos se guardan en un almacenamiento externo (S3, GCS, Azure).
*   **En Git:** Solo se guarda un pequeño archivo `.dvc` (un puntero) que contiene el hash del archivo de datos real.
*   **Ventaja:** Puedes hacer `git checkout` a una versión anterior y DVC descargará automáticamente los datos exactos que usaste en ese momento.

## 3. Versionado de Modelos
Un modelo no es solo un archivo `.pkl`. Es la combinación de:
*   **Código:** El script de entrenamiento.
*   **Datos:** El conjunto de datos usado.
*   **Configuración:** Los hiperparámetros elegidos.
Versionar el modelo significa guardar estas tres piezas unidas con un ID único.

## 4. El "Model Registry" (Registro de Modelos)
Es una base de datos centralizada donde guardamos los modelos listos para producción.
*   **Etiquetas:** Podemos marcar modelos como `Staging`, `Production` o `Archived`.
*   **Linaje:** El registro nos dice exactamente qué script y qué versión de los datos generó ese modelo.

## 5. Repositorios de Features (Feature Stores)
Como vimos en temas anteriores, el Feature Store también ayuda al versionado al garantizar que la definición de las variables no cambia entre el entrenamiento y la producción.

## Resumen: Trazabilidad Total
En un entorno profesional, "funcionaba en mi máquina" no es aceptable. El versionado de datos y modelos garantiza que cualquier experimento puede ser replicado, auditado y revertido en segundos si algo falla en el mundo real. Es la base de la seguridad en sistemas de IA.
