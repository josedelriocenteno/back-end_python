def insertar_ordenado(lista_ordenada, elemento):
    """
    Inserta 'elemento' manteniendo lista ORDENADA
    """
    # Encontrar posición correcta
    for i in range(len(lista_ordenada)):
        if lista_ordenada[i] > elemento:
            lista_ordenada.insert(i, elemento)
            return lista_ordenada
    
    # Si llega aquí, insertar al final
    lista_ordenada.append(elemento)
    return lista_ordenada

# PRUEBA
numeros = [1, 3, 5, 7, 9]
print("Original:", numeros)

insertar_ordenado(numeros, 4)  # Entre 3 y 5
print("Insertar 4:", numeros)  # [1, 3, 4, 5, 7, 9]

insertar_ordenado(numeros, 0)  # Al inicio
print("Insertar 0:", numeros)  # [0, 1, 3, 4, 5, 7, 9]

insertar_ordenado(numeros, 10) # Al final
print("Insertar 10:", numeros) # [0, 1, 3, 4, 5, 7, 9, 10]
