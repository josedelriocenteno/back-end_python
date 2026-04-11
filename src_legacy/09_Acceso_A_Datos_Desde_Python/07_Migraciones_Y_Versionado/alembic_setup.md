# Alembic Setup: El Estándar Profesional

Alembic es a SQLAlchemy lo que Git es a tu código. Permite que la base de datos evolucione junto con tus modelos del ORM de manera controlada y reversible.

## 1. Inicialización Recomendada

No uses el `alembic init` por defecto si quieres una estructura profesional.
```bash
# Crea la carpeta de migraciones y el archivo alembic.ini
alembic init alembic
```

## 2. Configuración en `alembic/env.py`

Este es el archivo más importante. Debes configurarlo para que Alembic "vea" tus modelos de SQLAlchemy.

```python
# alembic/env.py
from my_app.database import Base  # Importa tu DeclarativeBase
from my_app.models import *       # Importa TODOS tus modelos para que se registren

# Esto permite que Alembic autogenere migraciones comparando modelos vs DB
target_metadata = Base.metadata
```

## 3. Manejo de URLs Dinámicas

En lugar de poner la contraseña en `alembic.ini`, lee la URL de las variables de entorno para mayor seguridad.
```python
# alembic/env.py
import os
config.set_main_option("sqlalchemy.url", os.environ.get("DATABASE_URL"))
```

## 4. El Ciclo de Desarrollo

1.  **Cambio:** Modificas un atributo en un modelo (ej: `User.age`).
2.  **Revision:** Generas el script automáticamente.
    ```bash
    alembic revision --autogenerate -m "Add age to users"
    ```
3.  **Audit:** Abres el archivo en `versions/` y verificas que el SQL sea el correcto.
4.  **Upgrade:** Aplicas el cambio.
    ```bash
    alembic upgrade head
    ```

## 5. El archivo `script_location.py`

Puedes personalizar el formato de los nombres de los archivos de migración en `alembic.ini` para que incluyan la fecha, facilitando el orden cronológico.
`file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s`

## Resumen: Automatización sin Pérdida de Control

El setup correcto de Alembic es la diferencia entre un equipo que sufre con las bases de datos y un equipo que despliega cambios de esquema con total confianza. No olvides nunca registrar tus modelos en `env.py`; sin eso, el `--autogenerate` simplemente no funcionará.
