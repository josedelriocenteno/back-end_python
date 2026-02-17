# Compresión: Ahorrando bits y ganando segundos

La compresión reduce el tamaño de los datos en disco y red, pero consume CPU para comprimir y descomprimir. Elegir el algoritmo correcto es vital para no crear un nuevo cuello de botella.

## 1. El Trade-off: CPU vs. Espacio
*   **Más compresión:** Ocupa menos sitio pero tarda mucho más en comprimirse/descomprimirse.
*   **Menos compresión:** Es instantáneo pero el archivo es más grande.

## 2. Algoritmos Comunes en Data Engineering

### A. GZIP
*   **Uso:** El clásico. Mucha compresión.
*   **Problema:** No se puede "trocear" (Splittable). Si tienes un archivo GZIP de 10GB, solo un núcleo de CPU puede leerlo. Malo para el paralelismo.

### B. SNAPPY (El favorito de Google/Hadoop)
*   **Uso:** Optimizado para la velocidad extrema, no para el máximo ahorro de espacio.
*   **Ventaja:** Muy rápido y es splittable. Ideal para procesos paralelos masivos.

### C. ZSTD (El todoterreno moderno)
*   **Uso:** Creado por Facebook. Ofrece una tasa de compresión casi tan buena como GZIP pero es mucho más rápido descomprimiendo. Se está convirtiendo en el nuevo estándar.

## 3. Compresión en Tránsito
Asegúrate de que tus microservicios y APIs usen compresión (Gzip/Brotli) al enviarse datos JSON. Reducir el tráfico de red suele ser la forma más efectiva de ganar latencia en sistemas distribuidos.

## 4. Compresión en Bases de Datos
Bases de datos como PostgreSQL tienen compresión automática interna (`TOAST`). En Cloud SQL o BigQuery, la compresión es transparente para el usuario y está optimizada según el tipo de columna.

## 5. El error de comprimir lo comprimido
Nunca intentes comprimir archivos que ya lo están (como imágenes JPG o archivos comprimidos anteriormente). No ganarás nada de espacio y desperdiciarás ciclos de CPU convirtiendo el proceso en algo más lento.

## Resumen: Menos es Más Rápido
La compresión es tu aliada contra el cuello de botella del I/O (disco y red). En la mayoría de los casos de Big Data, pasar tiempo descomprimiendo en CPU es mucho más rápido que esperar a que el disco termine de leer un archivo gigante sin comprimir.
