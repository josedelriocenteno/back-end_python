from pathlib import Path

nombre_archivo = "archivo.txt"
ruta = Path(nombre_archivo)

if ruta.exists():
    print(f"El archivo {nombre_archivo} ya existe.")
else:
    ruta.write_text("Archivo creado automáticamente.")
    print(f"El archivo {nombre_archivo} ha sido creado.")