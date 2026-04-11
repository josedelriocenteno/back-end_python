def interseccion_listas(lista1, lista2):
    """
    Elementos COMUNES entre dos listas
    SIN sets. O(n*m)
    """
    comunes = []
    for elem1 in lista1:
        if elem1 in lista2 and elem1 not in comunes:
            comunes.append(elem1)
    return comunes

# PRUEBA
lista1 = [1, 2, 3, 4, 5]
lista2 = [4, 5, 6, 7, 8]

print(f"{lista1} ∩ {lista2} = {interseccion_listas(lista1, lista2)}")
# [4, 5]
