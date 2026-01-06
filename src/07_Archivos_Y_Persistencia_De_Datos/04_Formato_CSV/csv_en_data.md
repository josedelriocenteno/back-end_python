CSV en Data y ML: Casos Reales
1️⃣ Por qué CSV sigue siendo relevante

Aunque existen formatos más eficientes como Parquet o HDF5, CSV sigue siendo ampliamente usado por:

Su simplicidad y legibilidad.

Compatibilidad con Excel, Google Sheets, Python y R.

Intercambio rápido de datasets pequeños o medianos.

Pruebas rápidas en prototipos de ML.

2️⃣ Caso real 1: Dataset de entrenamiento de ML

Supongamos que tenemos un dataset de clientes para predecir churn:

id_cliente,nombre,edad,ultimo_login,compra_total
1,Juan,30,2025-01-01,150.75
2,Ana,25,2025-01-05,230.00
3,Luis,28,2024-12-20,0.00

Buenas prácticas:

Encabezados claros y consistentes.

Tipos correctos: edad → int, compra_total → float, fecha → string o datetime.

Sin celdas vacías si son obligatorias.

Guardar siempre con UTF-8.

Errores comunes:

Nombres de columnas inconsistentes (edad vs Edad).

Valores corruptos (NaN en string).

Fechas en formatos mixtos (2025-01-01 vs 01/01/2025).

3️⃣ Caso real 2: CSV como input para pipeline de ETL

Cuando un pipeline de ETL (Extract, Transform, Load) recibe CSV:

Extraer: leer CSV con DictReader o pandas.

Transformar: convertir tipos, normalizar datos, filtrar filas corruptas.

Cargar: insertar en base de datos o almacenar en Parquet para ML.

import csv

with open("clientes.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        try:
            fila["edad"] = int(fila["edad"])
            fila["compra_total"] = float(fila["compra_total"])
        except ValueError:
            continue  # Ignorar filas corruptas
        # Insertar en DB o guardar temporalmente


✅ Esta estrategia permite procesar datasets grandes sin saturar memoria.

4️⃣ Caso real 3: CSV en colaboración con Data Scientists

Equipo de backend exporta CSV a Data Science.

Equipo de DS importa CSV a pandas o NumPy.

Recomendaciones:

Columnas estandarizadas.

Separador claro (comma, ;).

Documentación de columnas (README o diccionario de datos).

5️⃣ CSV y reproducibilidad

Para garantizar reproducibilidad:

Mantener versiones de CSV (git o hash).

Documentar origen, fecha de extracción y transformación.

Evitar modificaciones manuales que rompan el esquema.

6️⃣ CSV vs otros formatos
Formato	Ventaja	Desventaja
CSV	Simple, universal	No soporta tipos complejos
JSON	Flexible, jerárquico	Más pesado para tablas grandes
Parquet	Columnar, eficiente	No legible directamente
Feather	Muy rápido para Python/pandas	Menos compatible fuera de Python

💡 Estrategia: usar CSV para intercambio y prototipos, y Parquet/Feather para producción y datasets grandes.

7️⃣ Buenas prácticas profesionales con CSV en Data

Validar siempre columnas y tipos.

Mantener encoding UTF-8.

Procesar CSV grandes fila a fila o por chunks.

Documentar significado de cada columna.

Evitar modificar CSV manualmente → usar scripts.

Versionar los CSV y almacenar hash o checksum para reproducibilidad.

Usar herramientas modernas como pandas, Dask o polars para datasets grandes.

8️⃣ Resumen

CSV sigue siendo clave en Data/ML por su simplicidad.

Validación, reproducibilidad y documentación son críticas.

Para proyectos grandes, siempre considerar streaming o conversión a formatos más eficientes.

Separar prototipo (CSV) de producción (Parquet, Feather) garantiza escalabilidad y estabilidad.