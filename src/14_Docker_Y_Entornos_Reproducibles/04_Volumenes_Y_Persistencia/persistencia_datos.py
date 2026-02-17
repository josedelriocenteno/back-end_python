"""
PERSISTENCIA DE DATOS: EJEMPLO PRÁCTICO
-----------------------------------------------------------------------------
Cómo configurar un script de Python para que guarde datos en un volumen.
"""

import os
import json
import time

# Definimos una ruta que mapearemos a un volumen en Docker
DATA_DIR = "/app/data"
FILE_PATH = os.path.join(DATA_DIR, "contador.json")

def asegurar_entorno():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Directorio {DATA_DIR} creado.")

def persistir_dato():
    asegurar_entorno()
    
    # Leemos el dato actual si existe
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
            contador = data.get("contador", 0)
    else:
        contador = 0
    
    # Incrementamos y guardamos
    contador += 1
    with open(FILE_PATH, "w") as f:
        json.dump({"contador": contador}, f)
    
    print(f"Contador persistido: {contador}")

if __name__ == "__main__":
    print("Script de persistencia arrancado...")
    while True:
        persistir_dato()
        time.sleep(5)

"""
INSTRUCCIONES PARA EJECUTAR CON PERSISTENCIA:
---------------------------------------------
1. Construye la imagen: 
   docker build -t mi-persistencia .

2. Ejecuta CON VOLUMEN (Los datos sobreviven si borras el contenedor):
   docker run -v contador_data:/app/data mi-persistencia

3. Ejecuta SIN VOLUMEN (Los datos se pierden al borrar el contenedor):
   docker run mi-persistencia
"""
