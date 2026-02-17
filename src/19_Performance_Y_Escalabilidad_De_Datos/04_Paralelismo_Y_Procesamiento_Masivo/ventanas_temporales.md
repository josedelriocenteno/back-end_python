# Ventanas Temporales y Procesamiento por Chunks

Cuando los datos no caben en la memoria RAM, debemos procesarlos por trozos (**Chunks**) o usando ventanas lógicas. Es una técnica vital para manejar archivos de varios GB con scripts sencillos.

## 1. Procesamiento por Chunks (Trozos)
En lugar de cargar un CSV de 10GB de una vez, lees 100.000 filas, las procesas, las guardas y las borras de la RAM para leer las siguientes 100.000.
```python
import pandas as pd

# Procesamos 10.000 filas cada vez sin saturar la RAM
for chunk in pd.read_csv("archivo_gigante.csv", chunksize=10000):
    procesar(chunk)
    guardar_en_db(chunk)
```

## 2. Ventanas en Streaming (Windowing)
En datos en tiempo real, no puedes "promediarlo todo" porque los datos nunca dejan de llegar. Usamos ventanas de tiempo:
*   **Tumbling Window (Ventana fija):** Cada 5 minutos fijos (00:00-00:05, 00:05-00:10).
*   **Sliding Window (Ventana deslizante):** "Los últimos 5 minutos" actualizados cada segundo.
*   **Session Window (Ventana de sesión):** Agrupa eventos mientras el usuario esté activo.

## 3. Manejo de Datos Tardíos (Late Data)
En sistemas masivos paralelos, el evento 1 puede llegar a las 10:05 aunque ocurrió a las 10:00 (por problemas de red).
*   **Watermark (Marca de agua):** Es una regla que le dice al sistema cuánto tiempo debe esperar a los datos tardíos antes de cerrar una ventana y dar el resultado por finalizado.

## 4. Deduplicación en Ventanas
El procesamiento paralelo a menudo genera duplicados. Usar ventanas permite identificar si ya hemos procesado ese mismo evento en el último rango de tiempo, manteniendo la integridad del dato final.

## 5. Ventanas en SQL
Las **Window Functions** (`OVER`, `PARTITION BY`, `ROWS BETWEEN`) permiten hacer cálculos complejos (medias móviles, rankings) sin colapsar el motor ni usar `GROUP BY` pesados.

## Resumen: Divide y Vencerás Temporalmente
Procesar por ventanas o trozos es la única forma de manejar lo infinitamente grande con recursos finitos. Es una técnica de ingeniería elegante que garantiza que tu sistema sea escalable y no dependa de tener una RAM infinita.
