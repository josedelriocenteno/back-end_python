# Alembic: Migraciones Reales con SQLAlchemy

Alembic es la herramienta de migraciones por excelencia en el ecosistema de Python cuando trabajas con SQLAlchemy. Permite trackear los cambios en tus modelos de Python y reflejarlos automáticamente en la base de datos.

## 1. Instalación e Inicialización

```bash
pip install alembic
alembic init alembic
```
Esto crea una carpeta `alembic/` con la configuración y una carpeta `versions/` donde vivirán tus scripts.

## 2. Configuración Clave

En `alembic.ini` defines la URL de tu base de datos, pero lo más profesional es configurarlo en `env.py` para que lea las variables de entorno de tu aplicación.

```python
# alembic/env.py
from my_app.models import Base
target_metadata = Base.metadata # Crucial para el autogenerate
```

## 3. El Flujo de Trabajo

### Paso 1: Generar la migración automáticamente
Alembic compara tus modelos de SQLAlchemy con la base de datos actual y genera el script.
```bash
alembic revision --autogenerate -m "Add status to users"
```

### Paso 2: Revisar el archivo generado
¡NUNCA confíes ciegamente en el autogenerate! Abre el archivo en `versions/` y verifica:
```python
def upgrade():
    op.add_column('users', sa.Column('status', sa.String(30), nullable=True))

def downgrade():
    op.drop_column('users', 'status')
```

### Paso 3: Aplicar la migración
```bash
alembic upgrade head
```

## 4. Comandos Profesionales Útiles

*   `alembic current`: Muestra en qué versión está tu DB ahora mismo.
*   `alembic history`: Lista todas las migraciones pasadas.
*   `alembic stamp head`: Marca la base de datos como "al día" sin ejecutar los scripts (útil si creaste las tablas manualmente por error).
*   `alembic downgrade -1`: Deshace la última migración aplicada.

## 5. Buenas Prácticas con Alembic

1.  **Nombres Descriptivos:** Usa mensajes claros en `-m`. "Init" no ayuda, "Create user and profile tables" sí.
2.  **Pequeñas y Frecuentes:** Es mejor tener 10 migraciones pequeñas que una gigante que cambie 20 tablas. Es más fácil de debuguear y de revertir.
3.  **Evita Lógica de Aplicación:** No importes funciones de tu app dentro de una migración (podrían cambiar en el futuro y romper la migración antigua). Usa SQL puro o las funciones `op` de Alembic.

## Resumen: Automatización con Control

Alembic te da la velocidad del autogenerado con el control total del SQL manual. Es una habilidad imprescindible para cualquier desarrollador backend senior que trabaje con el stack de SQLAlchemy.
