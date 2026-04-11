# Uso de Archivos .env en Backend Python

## 1. Introducción

Los archivos `.env` son la **herramienta estándar para gestionar variables de entorno** en proyectos profesionales.  
Permiten **separar configuración sensible del código**, facilitando seguridad, flexibilidad y portabilidad entre entornos.

> ⚠️ Nota:
> Nunca se deben subir archivos `.env` con datos sensibles a repositorios públicos. Se recomienda mantener un `.env.example` como referencia.

---

## 2. Qué es un archivo .env

- Es un archivo de texto plano que contiene **variables clave-valor**:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=supersecreto123
DEBUG=True
PORT=8000
Cada variable define un parámetro de configuración que puede cambiar según el entorno (desarrollo, staging, producción).

3. Integración en Python
3.1 Instalación de python-dotenv
bash
Copiar código
pip install python-dotenv
3.2 Carga de variables
python
Copiar código
from dotenv import load_dotenv
import os

# Carga variables desde el .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
PORT = int(os.getenv("PORT", 8000))
3.3 Uso en configuración por entorno
python
Copiar código
import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    from .production import *
else:
    from .development import *
4. Buenas prácticas profesionales
Ignorar .env en Git:

gitignore
Copiar código
.env
Mantener .env.example

Contiene todas las variables requeridas sin valores sensibles:

env
Copiar código
DATABASE_URL=
SECRET_KEY=
DEBUG=
PORT=
Validar variables al inicio de la aplicación:

python
Copiar código
required_vars = ["DATABASE_URL", "SECRET_KEY"]
for var in required_vars:
    if os.getenv(var) is None:
        raise EnvironmentError(f"La variable de entorno {var} no está definida")
Evitar cambios directos en producción

Usar herramientas de gestión de secretos (Vault, AWS Secrets Manager, GCP Secret Manager) para entornos críticos.

Seguridad

Nunca imprimir claves o tokens en logs.

Limitar permisos de archivos .env (600 en Linux).

5. Integración con flujo profesional
CI/CD

Variables de entorno deben ser configuradas en pipelines y no dentro del repositorio.

Ejemplo en GitHub Actions:

yaml
Copiar código
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
Testing

Crear .env.test para tests automatizados, cargando con load_dotenv(".env.test").

6. Errores comunes a evitar
Subir .env con credenciales reales a repositorios.

Hardcodear valores sensibles en código.

No documentar variables requeridas, generando confusión en equipo.

No validar variables, provocando errores en producción.

Usar el mismo .env para todos los entornos sin diferenciación.

7. Checklist rápido
 .env separado del código y ignorado en Git

 .env.example actualizado y completo

 Variables cargadas con python-dotenv

 Validación de variables al inicio de la aplicación

 Diferenciación de entornos (dev, test, prod)

 Integración segura con CI/CD y gestión de secretos

8. Conclusión
El uso correcto de archivos .env es crucial para mantener seguridad, flexibilidad y profesionalismo en proyectos backend Python.
Adoptar esta práctica permite que la configuración cambie sin afectar la lógica de negocio y protege información sensible.