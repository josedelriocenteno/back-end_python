formatos_de_datos.md
======================

# Formatos de Datos: Texto, Binario y Columnar

Cuando hablamos de **persistencia**, la forma en que almacenamos los datos tiene un gran impacto en:

- Velocidad de lectura y escritura
- Tamaño del archivo
- Facilidad de interoperabilidad
- Compatibilidad con otras herramientas y lenguajes

Existen tres grandes categorías de formatos:

1. **Texto plano**
2. **Binario**
3. **Columnar**

---

## 1️⃣ Formatos de texto plano

Ejemplos: `.txt`, `.csv`, `.json`, `.yaml`, `.xml`

### Características

- Human-readable: cualquier persona puede abrirlos y entenderlos.
- Interoperables entre lenguajes y sistemas.
- Más lentos de procesar para grandes volúmenes.
- Mayor tamaño en disco comparado con binario.
- Flexibles, fáciles de depurar.

### Ejemplo en Python: CSV y JSON

```python
import json
import csv

# JSON
data = {"nombre": "Juan", "edad": 30}
with open("usuario.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

with open("usuario.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(loaded_data)

# CSV
with open("usuarios.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["nombre", "edad"])
    writer.writerow(["Juan", 30])

Ventajas:

    Fácil de inspeccionar y modificar manualmente.

    Ideal para configuraciones, logs, APIs y datasets pequeños.

Desventajas:

    Más lento y pesado para grandes volúmenes.

    Parsing puede ser costoso.

2️⃣ Formatos binarios

Ejemplos: .pickle, .msgpack, .hdf5
Características

    No human-readable, almacenan datos en forma comprimida.

    Más rápidos de leer y escribir que texto.

    Pueden serializar objetos complejos directamente (listas, diccionarios, clases).

    Riesgo de incompatibilidad entre versiones de Python (por ejemplo con pickle).

Ejemplo en Python: Pickle

import pickle

data = {"nombre": "Juan", "edad": 30}

# Serializar a binario
with open("usuario.pkl", "wb") as f:
    pickle.dump(data, f)

# Leer de binario
with open("usuario.pkl", "rb") as f:
    loaded_data = pickle.load(f)
    print(loaded_data)

Ventajas:

    Velocidad de lectura/escritura superior a texto.

    Serialización directa de objetos complejos.

Desventajas:

    No es human-readable → difícil depurar sin herramientas.

    Riesgo de seguridad si se cargan datos de fuentes no confiables.

3️⃣ Formatos columnar (Columnar Storage)

Ejemplos: .parquet, .feather, .arrow
Características

    Almacenan datos por columna en lugar de por fila.

    Optimizado para procesamiento analítico y Big Data.

    Permite leer solo columnas necesarias → ahorro de memoria y velocidad.

    Compatible con herramientas de análisis como Pandas, Spark o Dask.

Ejemplo en Python: Parquet con Pandas

import pandas as pd

# Crear DataFrame
df = pd.DataFrame({
    "nombre": ["Juan", "Ana", "Luis"],
    "edad": [30, 25, 28],
    "ciudad": ["Madrid", "Barcelona", "Valencia"]
})

# Guardar en Parquet
df.to_parquet("usuarios.parquet", engine="pyarrow", index=False)

# Leer solo columna "nombre"
df_nombres = pd.read_parquet("usuarios.parquet", columns=["nombre"])
print(df_nombres)

Ventajas:

    Muy eficiente en lectura/escritura.

    Ideal para datasets grandes en análisis de datos y ML.

    Ahorro de memoria y espacio en disco.

Desventajas:

    No human-readable → depuración directa difícil.

    Requiere librerías externas (pyarrow, fastparquet).

4️⃣ Comparativa rápida
Formato	Legible por humano	Velocidad	Tamaño	Uso típico
Texto	✅ Sí	Medio	Grande	Config, logs, API, datasets pequeños
Binario	❌ No	Rápido	Medio	Serialización de objetos, ML intermedio
Columnar	❌ No	Muy rápido	Pequeño	Big Data, ML, análisis analítico
5️⃣ Buenas prácticas profesionales

    Elegir el formato según la necesidad:

        Configuración y APIs → JSON/YAML

        Datos temporales o experimentos → Pickle/MsgPack

        Big Data / ML → Parquet / Columnar

    Evitar sobreusar binario para datos que se pueden inspeccionar.

    Versionar datasets importantes y documentar estructura.

    Validar la integridad al leer/escribir.

    Combinar formatos: texto para config, binario/columnar para datos grandes.

    ✅ Conclusión:
    La elección del formato de datos afecta rendimiento, portabilidad y mantenibilidad. Un buen ingeniero de datos o desarrollador debe entender profundamente cada formato y cuándo usarlo para sistemas escalables y reproducibles.