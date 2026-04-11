valores = ["1", "2.5", "True", "None"]

# Función para convertir cada string al tipo correspondiente
def convertir_tipo(valor):
    if valor == "None":
        return None
    elif valor == "True":
        return True
    elif valor == "False":
        return False
    elif "." in valor:
        return float(valor)
    else:
        return int(valor)

# Convertir la lista
convertidos = [convertir_tipo(valor) for valor in valores]
print(convertidos)  # [1, 2.5, True, None]
