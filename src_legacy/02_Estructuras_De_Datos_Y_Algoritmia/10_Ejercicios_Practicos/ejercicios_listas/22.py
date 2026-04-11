def tiene_duplicados(lista):
    """
    Detecta DUPLICADOS comparando cada par
    SIN sets/diccionarios. O(n²)
    """
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True
    return False

# PRUEBA
lista1 = [1, 2, 3, 4]           # Sin duplicados
lista2 = [1, 2, 2, 4]           # Con duplicados
lista3 = [5, 5, 5, 5]           # Todos duplicados

print(f"{lista1} → {tiene_duplicados(lista1)}")  # False
print(f"{lista2} → {tiene_duplicados(lista2)}")  # True
print(f"{lista3} → {tiene_duplicados(lista3)}")  # True
