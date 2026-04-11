"""
MIGRACIONES Y ORM: CONFIGURACIÓN DINÁMICA
-----------------------------------------------------------------------------
Cómo usar Alembic desde código Python y personalizar las operaciones DDL.
"""

from alembic import op
import sqlalchemy as sa

# Ejemplo de un archivo de migración generado
# rev: 7de1a2b3c4d5
# down_revision: None

def upgrade():
    """
    Operaciones para subir de versión.
    Alembic nos da el objeto 'op' para ejecutar DDL de forma segura.
    """
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

def downgrade():
    """
    Operaciones para deshacer los cambios.
    """
    op.drop_table('users')

# TIP PROFESIONAL: Ejecutar comandos SQL puros en una migración
def upgrade_with_custom_sql():
    # Útil para crear extensiones o tipos complejos no soportados por op
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.add_column('users', sa.Column('bio', sa.Text()))

"""
QUÉ HACER SI EL AUTOGENERATE FALLA:
-----------------------------------------------------------------------------
Alembic no detecta TODO. Debes añadir manualmente:
1. Cambios en nombres de tablas o columnas (él verá un DROP y un CREATE).
2. Definiciones de Constraints complejas (CHECK).
3. Cambios en Enums específicos de Postgres.
"""

if __name__ == "__main__":
    # Recordatorio: Las migraciones se ejecutan desde el CLI de alembic,
    # no corriendo este archivo directamente.
    pass
