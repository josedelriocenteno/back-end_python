def detectar_y_convertir(elemento):
    # Intenta convertir a None
    if elemento.lower() in ("none", "null"):
        return None
    # Intenta convertir a booleano
    elif elemento.lower() in ("true", "false"):
        return elemento.lower() == "true"
    # Intenta convertir a entero
    elif elemento.isdigit():
        return int(elemento)
    # Intenta convertir a float
    try:
        return float(elemento)
    except ValueError:
        pass
    # Si no es ninguno de los anteriores, devuelve como string
    return elemento

# Ejemplo de uso
lista = ["10", "20.5", "True", "None", "Hola", "3.14", "abc"]
convertidos = [detectar_y_convertir(e) for e in lista]
print(convertidos)  # [10, 20.5, True, None, 'Hola', 3.14, 'abc']
