# SDK de Google Cloud para Python

Google ofrece bibliotecas de cliente oficiales para casi todos sus servicios. Usarlas es la forma profesional y segura de interactuar con la nube desde tu código de Python.

## 1. La filosofía "One Library per Service"
A diferencia de otras nubes que tienen una librería gigante (como Boto3 en AWS), Google prefiere librerías pequeñas y específicas. Esto hace que tu código sea más ligero y tenga menos conflictos de dependencias.
- `google-cloud-bigquery`
- `google-cloud-storage`
- `google-cloud-pubsub`
- `google-cloud-logging`

## 2. Instalación
Usa siempre un entorno virtual (`venv`) para no ensuciar el Python de tu sistema operativo.
```bash
pip install google-cloud-bigquery google-cloud-storage
```

## 3. Patrón de diseño: El Cliente (Client)
Todas las librerías de GCP siguen el mismo patrón. Primero creas un objeto `Client` y luego usas ese objeto para realizar acciones.
```python
from google.cloud import storage

# Creamos el cliente
client = storage.Client()

# Realizamos la acción
buckets = list(client.list_buckets())
print(f"Tienes {len(buckets)} buckets en tu proyecto.")
```

## 4. Documentación y Tipado
Las librerías modernas de Google tienen un excelente soporte para Type Hints. 
- **Tip:** Usa un editor como VS Code o PyCharm para que el autocompletado te ayude a ver qué parámetros acepta cada función (ej: nombres de datasets, configuraciones de carga).

## 5. El SDK de bajo nivel vs Alto nivel
- **Client Libraries:** (Recomendado). Diseñadas para humanos. Fáciles de usar.
- **REST Discovery API:** Para casos muy avanzados donde la librería oficial no ha implementado una función nueva todavía. Evítala si puedes.

## Resumen: Herramientas Oficiales
Usar las librerías oficiales de Google garantiza que tu código maneje correctamente la autenticación, los reintentos automáticos y las mejores prácticas de red de GCP. Es la base técnica de cualquier script de ingeniería de datos profesional.
