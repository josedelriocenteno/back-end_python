import pandas as pd
import numpy as np

def validar_datos(df):
    errors = []
    
    # 1. Chequeo de Nulos en columnas críticas
    null_counts = df['id_usuario'].isnull().sum()
    if null_counts > 0:
        errors.append(f"ERROR: Se encontraron {null_counts} nulos en id_usuario")

    # 2. Chequeo de Rangos (Edad entre 0 y 120)
    if not df['edad'].between(0, 120).all():
        invalid_ages = df[~df['edad'].between(0, 120)]['edad'].unique()
        errors.append(f"ERROR: Edades fuera de rango detectadas: {invalid_ages}")

    # 3. Chequeo de Formato (Email básico)
    if not df['email'].str.contains('@').all():
        errors.append("ERROR: Se detectaron emails sin formato válido")

    # 4. Chequeo de Unicidad
    if df['id_usuario'].duplicated().any():
        errors.append("ERROR: Hay IDs de usuario duplicados")

    return errors

if __name__ == "__main__":
    # Creamos un dataset de ejemplo con errores
    data = {
        'id_usuario': [1, 2, 2, 4, None],
        'edad': [25, 150, 30, -5, 40],
        'email': ['test@test.com', 'malo.com', 'ok@test.com', 'admin@web.es', 'user@co.uk']
    }
    df = pd.DataFrame(data)

    print("--- Iniciando Validación de Datos ---")
    resultados = validar_datos(df)
    
    if resultados:
        for err in resultados:
            print(err)
    else:
        print("¡Todo OK! Los datos son válidos.")
