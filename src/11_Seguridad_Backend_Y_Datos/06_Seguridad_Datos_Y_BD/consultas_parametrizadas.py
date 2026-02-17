"""
SEGURIDAD: CONSULTAS PARAMETRIZADAS (EL ANTÍDOTO)
-----------------------------------------------------------------------------
Cómo comunicarte con la base de datos de forma segura usando SQLAlchemy 
y Psycopg3.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

# 1. SQL PURO (PELIGROSO)
def search_user_dangerous(db: Session, username: str):
    # ¡NUNCA HAGAS ESTO! Concatenar variables es invitar a hackeos.
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(text(query)).all()

# 2. SQL PARAMETRIZADO CON TEXT (SEGURO)
def search_user_safe(db: Session, username: str):
    """
    Enviamos la query por un lado y los datos por otro. 
    La base de datos se encarga de que el dato sea tratado como texto plano, 
    no como código ejecutable.
    """
    query = text("SELECT * FROM users WHERE username = :name")
    # Los drivers se encargan de limpiar (sanitize) el valor ":name"
    return db.execute(query, {"name": username}).all()

# 3. CON EL ORM DE SQLALCHEMY (LO MÁS SEGURO)
def get_user_by_email(db: Session, email: str):
    """
    Usar el ORM es intrínsecamente seguro contra SQL Injection porque 
    siempre usa parámetros preparados por debajo.
    """
    return db.query(User).filter(User.email == email).first()

"""
REGLA DE ORO PARA EL DESARROLLADOR:
-----------------------------------------------------------------------------
- No confíes en ti mismo escapando caracteres manualmente.
- Usa placeholders (como :name, %s, o ?) dependiendo de tu driver.
- Si ves un 'f-string' o un '+' dentro de un db.execute(), hay una alarma 
  roja de seguridad.
"""

"""
RESUMEN:
La parametrización no solo es más segura, sino que también es más RÁPIDA. 
La base de datos guarda el 'Plan de Ejecución' de la query y solo cambia 
el dato, ahorrando tiempo de procesamiento en queries repetitivas.
"""
