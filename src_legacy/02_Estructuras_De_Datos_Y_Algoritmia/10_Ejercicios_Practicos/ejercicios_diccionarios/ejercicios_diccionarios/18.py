def aplanar_lista(lista_de_listas):
    """
    Aplana lista de listas → lista plana
    SIN itertools.chain
    """
    resultado = []
    for sublista in lista_de_listas:
        resultado.extend(sublista)  # Añade TODOS los elementos
    return resultado

# PRUEBA
datos_anidados = [
    [1, 2, 3],
    [4, 5],
    [6, 7, 8, 9],
    []  # Lista vacía OK
]

print("Anidado:", datos_anidados)
print("Plano:", aplanar_lista(datos_anidados))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
