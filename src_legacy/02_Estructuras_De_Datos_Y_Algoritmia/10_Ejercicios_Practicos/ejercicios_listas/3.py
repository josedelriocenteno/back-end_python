nombres = ["Alice", "Bob", "Carol", "David", "Eva"]

# Lista de tuplas: (string, longitud)
nombres_con_longitud = [(nombre, len(nombre)) for nombre in nombres]

print(nombres_con_longitud)
# Salida: [('Alice', 5), ('Bob', 3), ('Carol', 5), ('David', 5), ('Eva', 3)]
