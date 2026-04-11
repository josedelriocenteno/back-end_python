# Acceso a Cloud Storage desde Python

Como Data Engineer, usarás Python para mover archivos, limpiar carpetas y leer datos crudos directamente desde los Buckets de GCS.

## 1. Operaciones con Buckets y Blobs
En la SDK de Python, un archivo se llama **Blob** (Binary Large Object).
```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket("mi-bucket-de-datos")

# Crear un nuevo archivo (subir)
blob = bucket.blob("carpeta/nuevo_archivo.txt")
blob.upload_from_string("Contenido del archivo")

# Listar archivos
blobs = client.list_blobs("mi-bucket-de-datos", prefix="logs/")
for b in blobs:
    print(b.name)
```

## 2. Descarga y Lectura
Puedes bajar el archivo a tu disco local o leerlo directamente en memoria (streaming).
```python
# Bajar a disco
blob.download_to_filename("archivo_local.txt")

# Leer en memoria como string (para archivos pequeños)
data = blob.download_as_text()
```

## 3. Streaming de Datos (Grandes archivos)
Si el archivo es muy grande (ej: 10GB de CSV), no lo bajes entero a RAM. Usa un flujo de lectura:
```python
# Útil para procesar línea a línea
with blob.open("r") as f:
    for line in f:
        process(line)
```

## 4. Gestión de Metadatos
Puedes cambiar etiquetas o el tipo de contenido de un archivo sin descargarlo:
```python
blob.metadata = {"equipo": "data", "calidad": "alta"}
blob.patch()
```

## 5. Generar Signed URLs
Puedes generar el enlace temporal que vimos en la sección 03 desde Python:
```python
from datetime import timedelta

url = blob.generate_signed_url(expiration=timedelta(minutes=15), method="GET")
print(f"Enlace temporal: {url}")
```

## Resumen: Fontanería de Archivos
La SDK de Cloud Storage para Python es robusta y eficiente. Te permite automatizar la organización de tu Data Lake, realizar tareas de limpieza y servir datos de forma segura a usuarios externos con unas pocas líneas de código.
