def copia_profunda_iterativa(lista):
    nueva = []
    for elem in lista:
        if isinstance(elem, list):
            nueva.append(elem[:])  # Copia superficial de sublistas
        else:
            nueva.append(elem)
    return nueva
