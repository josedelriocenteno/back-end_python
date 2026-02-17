"""
PSYOOPG 3: MANEJO DE ERRORES DE BASE DE DATOS
-----------------------------------------------------------------------------
No todos los errores son iguales. Capturar errores específicos nos permite
dar feedback real al usuario (ej: "Ese email ya existe").
"""

import psycopg
from psycopg import errors

DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

def error_handling_examples():
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                # Intentamos insertar un usuario duplicado
                cur.execute("INSERT INTO users (username) VALUES ('alice')")
    
    # 1. Error de Violación de Restricción Única (UniqueViolation)
    except errors.UniqueViolation as e:
        print("ERROR: El nombre de usuario ya está en uso.")
    
    # 2. Error de Clave Foránea (ForeignKeyViolation)
    except errors.ForeignKeyViolation as e:
        print("ERROR: Estás intentando referenciar un registro que no existe.")
    
    # 3. Error de Tipos o Datos Inválidos (DataError / CheckViolation)
    except errors.CheckViolation as e:
        print("ERROR: Los datos no cumplen las reglas de validación.")

    # 4. Error de Conexión (OperationalError)
    except psycopg.OperationalError as e:
        print(f"ERROR DE RED/DB: {e}")

    # 5. Captura genérica de base de datos
    except psycopg.Error as e:
        print(f"Ocurrió un error inesperado en Postgres: {e.pgcode} - {e}")

"""
RESUMEN PARA EL DESARROLLADOR:
1. El módulo 'psycopg.errors' contiene excepciones para casi cada código de SQL.
2. Capturar 'UniqueViolation' es vital para APIs que gestionan registros únicos.
3. Siempre loguea el 'pgcode' en tus sistemas de monitoreo; es la clave para 
   entender qué fue mal en la DB.
"""

if __name__ == "__main__":
    error_handling_examples()
