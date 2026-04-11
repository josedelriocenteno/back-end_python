def mi_insert(lista, indice, valor):
    """
    Inserta 'valor' en 'indice' SIN usar insert()
    Coste: O(n) - mueve n-indice elementos
    """
    # Crear nueva lista con espacio para el nuevo elemento
    nueva_lista = [None] * (len(lista) + 1)
    
    # Copiar elementos ANTES del índice
    for i in range(indice):
        nueva_lista[i] = lista[i]
    
    # Insertar el nuevo valor
    nueva_lista[indice] = valor
    
    # Copiar elementos DESPUÉS del índice
    for i in range(indice, len(lista)):
        nueva_lista[i + 1] = lista[i]
    
    return nueva_lista

# PRUEBA
lista = [1, 2, 3, 4, 5]
print("Original:", lista)

# Insertar en posición 2 (principio → más caro)
resultado1 = mi_insert(lista, 2, 99)
print("Insertar en idx=2:", resultado1)  # [1, 2, 99, 3, 4, 5]

# Insertar al final (más barato)
resultado2 = mi_insert(lista, len(lista), 100)
print("Insertar al final:", resultado2)  # [1, 2, 3, 4, 5, 100]
