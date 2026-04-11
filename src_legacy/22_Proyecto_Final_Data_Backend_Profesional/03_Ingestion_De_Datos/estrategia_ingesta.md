# Ingesta de Datos: Alimentando el Motor

Sin datos de calidad, no hay inteligencia. En esta sección implementarás la tubería de entrada de información.

## 1. Estrategia de Ingesta
No vamos a descargar internet entero. Nos centraremos en fuentes estructuradas para garantizar la limpieza:
*   **APIs Financieras:** (ej: Alpha Vantage, Yahoo Finance).
*   **RSS Feeds:** Noticias tecnológicas o económicas.
*   **Archivos Locales:** Un dataset inicial en Parquet para probar el sistema sin conexión.

## 2. El Ciclo de Vida del Dato (ETL)

### Extract (Extracción)
*   Usa la librería `requests` de Python.
*   Implementa **Manejo de Errores** robusto: Si la API de noticias cae, el sistema no debe romperse, debe esperar y reintentar (exponential backoff).

### Transform (Transformación)
*   **Limpieza:** Usa `Pandas` para eliminar duplicados y nulos.
*   **Enriquecimiento:** Usa la IA (modelos pequeños) para clasificar la noticia antes de guardarla.
*   **Chunking:** Divide la noticia en fragmentos de ~1000 tokens para que entren bien en la memoria de la Vector DB.

### Load (Carga)
*   Guarda los metadatos en SQL.
*   Guarda los vectores en la Vector DB.
*   **Atomicidad:** Asegúrate de que si la carga falla, no se queden datos a medias.

## 3. Automatización
Tu ingesta no debe ser manual. Usa:
*   Un script que se ejecute cada hora.
*   Un log detallado que te avise si una fuente de datos empieza a fallar.

---

## Punto de Control
Al terminar esta sección, deberías poder entrar en tu base de datos y ver las últimas 50 noticias de "Inteligencia Artificial" listas para ser consultadas por la API.
