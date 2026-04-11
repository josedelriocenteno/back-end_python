"""
DATA ENGINEERING: INTEGRACIÓN CON PANDAS
-----------------------------------------------------------------------------
SQLAlchemy es el motor preferido de Pandas para leer y escribir DataFrames.
"""

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://user:pass@localhost/db")

# 1. LEER DE SQL A DATAFRAME
def sql_to_pandas():
    # Podemos pasar una query de texto o un objeto select() de SQLAlchemy
    query = "SELECT * FROM users WHERE is_active = true"
    
    df = pd.read_sql(query, engine)
    print(f"Cargadas {len(df)} filas en el DataFrame.")
    return df

# 2. ESCRIBIR DE DATAFRAME A SQL
# Ideal para cargar resultados de procesos de analítica o limpieza.
def pandas_to_sql(df: pd.DataFrame):
    # if_exists: 'fail' (error si existe), 'replace' (borra y crea), 'append' (añade)
    df.to_sql(
        "users_analytics", 
        engine, 
        if_exists="append", 
        index=False,
        chunksize=1000, # Muy importante para no saturar memoria
        method="multi"  # Inserta varias filas por cada comando INSERT (más rápido)
    )

"""
NOTAS DE RENDIMIENTO:
-----------------------------------------------------------------------------
'to_sql' por defecto de Pandas puede ser lento en Postgres. 
Para optimizarlo, se recomienda definir una función 'method' personalizada 
que use el comando 'COPY' de Postgres.
"""

"""
RESUMEN PARA EL DATA ENGINEER:
1. 'read_sql' es la forma más rápida de volcar datos a Pandas.
2. Siempre usa 'chunksize' al escribir DataFrames pesados.
3. 'method="multi"' es una ganancia de velocidad fácil en versiones modernas de Pandas.
4. Asegúrate que los nombres de las columnas del DataFrame coincidan con los de la tabla.
"""
