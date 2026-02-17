# El Coste del Almacenamiento: Datos Fríos vs Calientes

Guardar datos es cada vez más barato, pero guardar PETABYTES de datos sigue siendo caro si no se hace con inteligencia.

## 1. Las capas de almacenamiento (Storage Tiers)
No todos los datos se usan con la misma frecuencia.
*   **Hot (Caliente):** Acceso constante. Caro de guardar, barato de leer. (Cloud Storage Standard).
*   **Cold (Frío):** Acceso una vez al mes. Barato de guardar, más caro de leer. (Nearline).
*   **Archive (Archivo):** Acceso una vez al año (copias de seguridad legales). Muy barato de guardar, pero cuesta mucho tiempo y dinero recuperar los datos.

## 2. El Ciclo de Vida del Dato (Lifecycle Policies)
No dejes que el cubo de basura se llene.
*   **Regla automática:** "Mueve los archivos de este bucket a la capa Archive si llevan 60 días sin ser consultados".
*   **Regla automática:** "Borra los logs temporales tras 7 días".
Esto mantiene el coste bajo control de forma totalmente automática.

## 3. Compresión: Menos es Más
Comprimir los datos (ej: usando formato **Parquet** con compresión Snappy o Gzip) puede reducir el espacio ocupado en un 70-80%.
*   En la nube pagas por GB, así que comprimir es la mejor inversión. Como beneficio extra, leer archivos comprimidos suele ser más rápido porque hay que mover menos datos por la red.

## 4. Costes de Red (Egress)
Mover datos DENTRO de la misma región suele ser gratis o muy barato.
*   **Peligro:** Enviar datos de un servidor en EE.UU. a uno en Europa cuesta mucho dinero (**Egress Costs**).
*   **Estrategia:** Mantén tus procesos de datos y tus bases de datos en la misma región siempre que sea posible.

## 5. Almacenamiento en Bases de Datos
En SQL (Postgres/BigQuery), el espacio en disco también se paga.
*   Borra índices que no uses.
*   Limpia tablas temporales tras la carga del pipeline.

## Resumen: Orden y Limpieza
Gestionar el almacenamiento es una tarea de mantenimiento constante. Usar las capas adecuadas, comprimir la información y tener políticas claras de borrado evita que los costes de almacenamiento crezcan de forma exponencial y asegura que solo pagas por la información que realmente aporta valor.
