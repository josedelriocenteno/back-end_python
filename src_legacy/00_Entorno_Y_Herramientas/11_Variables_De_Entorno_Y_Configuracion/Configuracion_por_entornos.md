# Configuración por Entornos en Backend Python

## 1. Introducción

La **configuración por entornos** es una práctica profesional que permite ejecutar la misma aplicación en **desarrollo, testing y producción** sin modificar el código fuente.  
Esto asegura **seguridad, consistencia y facilidad de despliegue**.

> ⚠️ Nota:
> Separar entornos evita errores críticos, exposición de datos sensibles y conflictos entre equipos.

---

## 2. Principio de configuración por entornos

1. **Entorno de desarrollo**  
   - Optimizado para depuración y desarrollo rápido.  
   - `DEBUG=True`, base de datos local o sandbox.  

2. **Entorno de testing**  
   - Simula producción pero con datos ficticios.  
   - Permite ejecutar **tests automatizados** sin afectar usuarios reales.  

3. **Entorno de producción**  
   - Configuración real, segura y optimizada.  
   - `DEBUG=False`, logging y monitoreo activados.  

```text
.env.development
.env.test
.env.production
3. Estrategia profesional para configurar entornos
3.1 Archivos de configuración separados
Crear archivos por entorno en config/:

python
Copiar código
# config/development.py
DEBUG = True
DATABASE_URL = "postgresql://dev_user:dev_pass@localhost:5432/dev_db"
LOG_LEVEL = "DEBUG"

# config/test.py
DEBUG = False
DATABASE_URL = "postgresql://test_user:test_pass@localhost:5432/test_db"
LOG_LEVEL = "WARNING"

# config/production.py
DEBUG = False
DATABASE_URL = "postgresql://prod_user:prod_pass@prod_host:5432/prod_db"
LOG_LEVEL = "ERROR"
Selección dinámica:

python
Copiar código
import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    from .production import *
elif ENV == "test":
    from .test import *
else:
    from .development import *
3.2 Uso de .env por entorno
Archivos .env.development, .env.test y .env.production:

env
Copiar código
# .env.development
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/dev_db
SECRET_KEY=dev_secret
DEBUG=True
Cargar variables según entorno:

python
Copiar código
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")
load_dotenv(f".env.{ENV}")
4. Beneficios de la configuración por entornos
Seguridad

Contraseñas y claves de producción nunca se mezclan con desarrollo o testing.

Flexibilidad

Cambiar entre entornos sin modificar código.

Escalabilidad

Permite múltiples instancias de la aplicación en distintos entornos controlados.

Facilidad de CI/CD

Variables de entorno inyectadas automáticamente en pipelines de integración y despliegue.

5. Buenas prácticas profesionales
Mantener archivos .env.example actualizados para cada entorno.

Validar todas las variables críticas al inicio de la aplicación:

python
Copiar código
required_vars = ["DATABASE_URL", "SECRET_KEY"]
for var in required_vars:
    if os.getenv(var) is None:
        raise EnvironmentError(f"La variable de entorno {var} no está definida")
No subir archivos .env con datos sensibles a repositorios.

Documentar diferencias entre entornos para el equipo.

Integrar variables de entorno en CI/CD y despliegues automatizados.

6. Errores comunes a evitar
Usar la misma configuración para todos los entornos.

Hardcodear credenciales de producción en desarrollo.

No validar variables al iniciar la aplicación.

Exponer secretos en logs o errores.

Mezclar datos de testing con producción.

7. Checklist rápido
 Archivos de configuración separados por entorno

 Variables críticas definidas y validadas al inicio

 .env y secretos ignorados en Git

 Diferenciación clara entre desarrollo, test y producción

 Configuración integrada en pipelines CI/CD

 Documentación de variables y diferencias por entorno

8. Conclusión
La configuración por entornos garantiza que la aplicación backend Python sea segura, flexible y escalable.
Adoptar esta práctica profesional es crucial para trabajar en entornos reales de producción y mantener consistencia entre equipos y pipelines de CI/CD.