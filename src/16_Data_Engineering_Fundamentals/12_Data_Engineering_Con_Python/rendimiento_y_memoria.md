# Rendimiento y Optimización de Memoria

El mayor enemigo del Data Engineer en Python es el error `OutOfMemory` (OOM). Aprender a gestionar la memoria es la diferencia entre un pipeline que escala y uno que explota.

## 1. Lectura por Trozos (Chunking)
Nunca leamos un archivo de 20GB de golpe si nuestra RAM es de 8GB.
- **Técnica:** Lee el archivo en trozos de 100.000 filas, procésalos y escribe el resultado antes de leer el siguiente trozo.
```python
# En Pandas
for chunk in pd.read_csv("gigante.csv", chunksize=100000):
    process(chunk)
```

## 2. Tipos de Datos Eficientes (Dtypes)
Python usa por defecto tipos muy pesados.
- Un número de 0 a 100 no necesita un `int64` (8 bytes). Basta con un `int8` (1 byte).
- Si una columna de texto tiene pocos valores repetidos (ej: "Hombre", "Mujer"), conviértela a tipo `Category`. Reduce el uso de memoria en un 90%.

## 3. Evita Copias Innecesarias
Cada vez que haces `df2 = df1[df1['ventas'] > 100]`, Python crea una copia de los datos en memoria.
- Usa `inplace=True` (donde esté disponible) o libera memoria manualmente borrando variables con `del df1` seguidos de un llamado al recolector de basura `gc.collect()`.

## 4. Memory Mapping
Librerías como PyArrow permiten "mapear" archivos en disco como si estuvieran en memoria. El sistema operativo carga solo las partes que estás leyendo en ese momento, permitiendo procesar archivos Terabytes más grandes que tu RAM física.

## 5. Profiling: Encuentra el cuello de botella
Usa herramientas como `memory_profiler` para ver exactamente qué línea de tu código está consumiendo más memoria.
- **Recuerda:** Optimiza solo lo que hace falta. No gastes horas ahorrando 1MB si te sobran 32GB de RAM.

## Resumen: Eficiencia es Supervivencia
Optimizar no es solo para ir más rápido, es para que el código sea viable. Un pipeline eficiente es más barato de ejecutar en la nube y mucho más fiable bajo condiciones de alta carga.
