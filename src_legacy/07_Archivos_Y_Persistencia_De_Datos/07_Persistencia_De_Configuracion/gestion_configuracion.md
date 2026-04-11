gestion_configuracion.md
Estrategia profesional de gestión de configuración en proyectos Python
1️⃣ Por qué la configuración importa de verdad

En proyectos medianos y grandes, la configuración no es un lujo, es parte del sistema. Si la gestionas mal:

Tu aplicación no es reproducible.

Cambiar entornos (dev, staging, prod) se vuelve un dolor.

Introduces bugs sutiles, difíciles de debuggear.

Los pipelines de ML o Data pueden romperse silenciosamente.

Un buen manejo de configuración te da:

Claridad: todo está en un lugar predecible.

Seguridad: secretos no se filtran.

Portabilidad: el mismo código corre en distintos entornos sin cambios manuales.

Reproducibilidad: datos, modelos y logs consistentes.

2️⃣ Jerarquía de configuración profesional

En un proyecto real, puedes combinar distintos tipos de archivos según su propósito:

Tipo	Cuándo usar	Ejemplo
.env	Secretos y variables simples	DB_PASSWORD, API_KEY
.ini	Configuración estructurada pequeña	DB_HOST, DB_PORT, DEBUG
.yaml / .yml	Configuración compleja, pipelines ML, listas y dicts anidados	ML parameters, feature flags, modules

Regla de oro: separar la configuración por propósito, no meter todo en un solo archivo.

3️⃣ Estructura de proyecto recomendada
project/
├── config/
│   ├── .env                  # Secretos
│   ├── app.ini                # Config simple de app
│   └── ml_pipeline.yaml       # Config compleja de ML/Data
├── src/
│   ├── main.py
│   └── modules/
└── tests/


config/ es el punto único de entrada de la configuración.

Siempre usar pathlib para acceder a archivos de forma portable.

Validar que cada archivo exista antes de usarlo.

4️⃣ Buenas prácticas de carga

Validar existencia del archivo antes de leerlo.

Usar safe loaders (yaml.safe_load) para evitar ejecución de código.

Convertir tipos explícitamente, no asumir strings mágicas.

Valores por defecto (fallback en configparser, dict.get en YAML) para entornos incompletos.

No hardcodear secretos en ningún lado, usar .env + python-dotenv.

Ejemplo conceptual:

# config_loader.py
from pathlib import Path
import yaml
import configparser
from dotenv import load_dotenv
import os

# 1️⃣ Cargar .env
load_dotenv(Path("config/.env"))

# 2️⃣ Cargar INI
config_ini = configparser.ConfigParser()
config_ini.read(Path("config/app.ini"))

# 3️⃣ Cargar YAML
with open(Path("config/ml_pipeline.yaml"), "r") as f:
    config_yaml = yaml.safe_load(f)

# 4️⃣ Combinar/validar
db_host = config_ini.get("database", "host", fallback="localhost")
api_key = os.getenv("API_KEY")
batch_size = config_yaml.get("ml_pipeline", {}).get("batch_size", 32)

5️⃣ Validación y fail-fast

Nunca asumas que el archivo está bien escrito.

Validar tipos y existencia de secciones al inicio.

Fallar rápido si algo crítico falta:

if not api_key:
    raise RuntimeError("API_KEY no está configurada en .env")


Esto evita que errores aparezcan más tarde, en producción o en un entrenamiento ML que tarde horas.

6️⃣ Seguridad

Nunca pongas datos sensibles en YAML o INI.

Solo en .env y con permisos restringidos.

Siempre limpiar archivos temporales después de tests o pipelines (tmp/).

7️⃣ Configuración por entorno

Mantener archivos separados por entorno es más limpio que condicionales en el código:

config/
├── dev/
│   ├── app.ini
│   └── ml_pipeline.yaml
├── prod/
│   ├── app.ini
│   └── ml_pipeline.yaml


Elegir el entorno con variable de entorno: ENV=dev o ENV=prod.

8️⃣ Resumen de reglas de oro

Separar secretos, configuración simple y compleja.

Usar librerías correctas: dotenv, configparser, pyyaml.

Validar todo: existencia, tipo, estructura.

Fail-fast: detectar errores de configuración al inicio.

Versionar archivos de configuración, excepto secretos.

Evitar hardcodear cualquier valor en el código.