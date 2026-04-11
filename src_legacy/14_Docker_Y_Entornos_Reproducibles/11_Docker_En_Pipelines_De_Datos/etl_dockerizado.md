# ETL Dockerizado: La unidad de procesamiento

En ingeniería de datos, un proceso ETL (Extract, Transform, Load) a menudo debe correr en entornos muy diferentes (Staging con datos pequeños, Producción con datos masivos). Docker es el puente que garantiza el éxito.

## 1. El reto de las librerías científicas
Si tu ETL usa Pandas, NumPy o PyTorch, instalarlas en un servidor a pelo es una pesadilla de dependencias de C++.
- **Ventaja Docker:** Construyes la imagen una vez, confirmas que las librerías funcionan, y esa imagen correrá igual en tu portátil que en un clúster de Spark.

## 2. Parámetros por Variables de Entorno
Tu ETL no debe tener rutas hardcodeadas.
```python
import os
INPUT_PATH = os.getenv("SOURCE_BUCKET", "/data/input")
OUTPUT_PATH = os.getenv("DEST_BUCKET", "/data/output")
```
Esto permite que el mismo contenedor lea de una carpeta local en tu PC (Bind Mount) o de un bucket de S3 en la nube sin cambiar el código.

## 3. Manejo de Volúmenes para Datos Gigantes
Si tu ETL procesa 100GB de datos, **no los metas dentro de la imagen**.
- Usa volúmenes para que el contenedor lea directamente del disco del servidor.
- `docker run -v /nfs/shared_data:/data etl_image`

## 4. El contenedor como "Tarea Única"
A diferencia de una API que corre siempre, un contenedor de ETL nace, procesa y muere.
- **Tip Senior:** Asegúrate de que tu script de Python devuelve un código de salida correcto (`exit 0` si fue bien, `exit 1` si falló) para que el orquestador sepa si el trabajo se completó.

## 5. Logging y Auditoría
En Data Pipelines, el log es el "ticket" de que los datos son correctos.
- Usa el formato JSON en los logs para que herramientas de monitorización puedan parsear cuántas filas se procesaron o si hubo errores de esquema.

## Resumen: Portabilidad del Dato
Dockerizar tus ETLs te permite desacoplar los procesos del hardware. Puedes mover tu procesamiento de un servidor barato a una máquina con 256GB de RAM en segundos simplemente cambiando dónde lanzas el contenedor.
