def eliminar_valores_duplicados(lista):
    resultado = []
    for i in lista:
        if i not in resultado:
            resultado.append(i)
    return resultado

lista = [1, 3, 3, 2, 1, 4, 3, 2, 5]
print("Original:", lista)
print("Sin duplicados:", eliminar_valores_duplicados(lista))