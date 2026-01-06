Versionado de Archivos
1️⃣ Introducción

En proyectos de software, data o ML, los archivos cambian con el tiempo: logs, datasets, modelos, configuraciones.
El versionado de archivos permite:

Saber qué cambió y cuándo.

Recuperar versiones anteriores.

Evitar sobreescritura accidental.

Facilitar reproducibilidad en pipelines de datos.

Existen dos niveles principales:

Versionado manual: incluir un número de versión o timestamp en el nombre del archivo.

Versionado automatizado / con herramientas: usar Git, DVC, S3 versioning, etc.

2️⃣ Versionado manual
Estrategias comunes

Timestamps:

dataset_2026-01-06.csv
log_2026-01-06_14-30.txt


Ventajas:

Fácil de implementar.

Funciona sin herramientas externas.

Desventajas:

Difícil de rastrear cambios de contenido.

Puede generar archivos redundantes si no se limpia.

Números de versión:

modelo_v1.pkl
modelo_v2.pkl


Ventajas:

Claro para modelos iterativos.

Simple de automatizar.

Desventajas:

No indica fecha ni contenido exacto.

Requiere disciplina en la numeración.

3️⃣ Versionado con herramientas
3.1 Git / Git LFS

Git permite versionar archivos de código y pequeños datos.

Para archivos grandes, usar Git LFS:

Almacena los binarios fuera del repositorio.

Mantiene histórico sin sobrecargar Git.

3.2 DVC (Data Version Control)

Ideal para datasets y modelos grandes.

Integra con Git para trackear cambios en datos.

Permite:

Versionar datasets.

Reproducir experimentos.

Compartir datos en equipo de manera controlada.

3.3 Versionado en Cloud (S3, GCS, Azure Blob)

Muchos servicios cloud ofrecen versioning nativo.

Ejemplo: en S3, activar versioning en un bucket:

Cada actualización de un archivo genera una nueva versión.

Se puede restaurar cualquier versión anterior.

Ventajas:

Escalable y distribuido.

Integración con pipelines de producción.

4️⃣ Buenas prácticas de versionado

No sobreescribir archivos críticos: siempre guardar nueva versión.

Nombrado consistente: usar esquema uniforme (nombre_tipo_fecha.ext o nombre_vX.ext).

Mantener histórico limitado: limpiar versiones antiguas si ocupan mucho espacio.

Automatizar versionado:

Scripts que agreguen timestamp o incrementen versión automáticamente.

Integración con CI/CD:

Subir versiones de datos/modelos junto con código.

Documentar cambios: guardar un log de cambios (changelog) para datasets importantes.

5️⃣ Ejemplo práctico de versionado manual en Python
from pathlib import Path
from datetime import datetime
import shutil

# Carpeta donde se guardan los datasets
DATA_DIR = Path("data/")
DATA_DIR.mkdir(exist_ok=True)

# Dataset original
archivo_original = DATA_DIR / "dataset.csv"

# Generar versión con timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
archivo_version = DATA_DIR / f"dataset_{timestamp}.csv"

# Copiar archivo original a versión
shutil.copy(archivo_original, archivo_version)
print(f"Archivo versionado como: {archivo_version}")


Con este enfoque, cada vez que proceses o actualices un dataset, puedes guardar una versión nueva con timestamp.

6️⃣ Conclusión

El versionado de archivos y datos es clave para proyectos reproducibles, escalables y seguros.

Para proyectos pequeños → versionado manual o Git LFS.

Para proyectos de ML/Data con datos grandes → DVC o versioning en cloud.

Mantener convenciones claras y consistencia evita pérdidas y errores en producción.