# Separar Código y Configuración en Backend Python

## 1. Introducción

Separar **código** y **configuración** es una práctica fundamental en proyectos profesionales.  
Permite **flexibilidad, seguridad y escalabilidad**, evitando que cambios en configuración afecten directamente al código fuente.

> ⚠️ Nota:
> Mezclar configuración y código genera errores, hace difícil cambiar entornos y expone secretos accidentalmente.

---

## 2. Principio de separación

1. **Código**  
   - Contiene la **lógica de negocio**, funciones, clases y módulos que implementan funcionalidades.  

2. **Configuración**  
   - Contiene **variables dependientes del entorno**, como credenciales, URLs de servicios, parámetros de API, etc.

```text
# Código
app/main.py
app/services/auth.py

# Configuración
.env
config/settings.py
3. Estrategias profesionales para separar configuración
3.1 Variables de entorno
Guardar secretos, credenciales y URLs sensibles en .env:

env
Copiar código
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=supersecreto123
DEBUG=True
Cargar variables en Python con python-dotenv:

python
Copiar código
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
3.2 Archivos de configuración por entorno
Crear archivos distintos para cada entorno (development.py, production.py):

python
Copiar código
# config/development.py
DEBUG = True
DATABASE_URL = "postgresql://dev_user:dev_pass@localhost:5432/dev_db"

# config/production.py
DEBUG = False
DATABASE_URL = "postgresql://prod_user:prod_pass@prod_host:5432/prod_db"
Selección dinámica en settings.py:

python
Copiar código
import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    from .production import *
else:
    from .development import *
4. Beneficios de la separación profesional
Seguridad

No hardcodear credenciales en el código.

Flexibilidad

Cambiar entornos (desarrollo, staging, producción) sin tocar código.

Mantenibilidad

Configuración centralizada, fácil de auditar y modificar.

Facilidad en despliegue y CI/CD

Variables de entorno inyectadas automáticamente en pipelines de CI/CD.

5. Buenas prácticas profesionales
Usar .env y archivos de configuración ignorados en Git.

Nunca subir secretos a repositorio.

Documentar todas las variables necesarias por entorno en README o .env.example.

Evitar condicionales complejas de entorno dentro del código; usar módulos de configuración.

Validar variables al inicio de la aplicación:

python
Copiar código
required_vars = ["DATABASE_URL", "SECRET_KEY"]
for var in required_vars:
    if os.getenv(var) is None:
        raise EnvironmentError(f"Variable de entorno {var} no definida")
6. Errores comunes a evitar
Hardcodear credenciales en código.

Mezclar parámetros de entorno con lógica de negocio.

Subir .env o archivos sensibles al repositorio.

No documentar variables requeridas para distintos entornos.

Modificar configuración directamente en producción sin control.

7. Checklist rápido
 Código y configuración completamente separados

 .env y archivos de configuración ignorados en Git

 Variables de entorno documentadas y validadas

 Archivos de configuración por entorno (development.py, production.py)

 Configuración inyectada en pipelines de CI/CD correctamente

 Seguridad: ninguna credencial hardcodeada en código

8. Conclusión
Separar código y configuración es una práctica profesional imprescindible en backend Python.
Permite seguridad, flexibilidad y mantenibilidad, y es esencial para trabajar en equipos grandes y entornos de producción reales.