# Lista inicial
lista = [1, 2, 3]

print("Antes:", lista)

# SIMULAR append(4) SIN usar append()
nuevo_tamaño = len(lista)  # 3
lista[nuevo_tamaño:nuevo_tamaño+1] = [4]  # Extiende con [4]

print("Después de 'append(4)':", lista)  # [1, 2, 3, 4]

# SIMULAR append(5)
nuevo_tamaño = len(lista)  # 4
lista[nuevo_tamaño:nuevo_tamaño+1] = [5]

print("Después de 'append(5)':", lista)  # [1, 2, 3, 4, 5]

# FUNCIÓN que simula append()
def mi_append(lista, elemento):
    nuevo_tamaño = len(lista)
    lista[nuevo_tamaño:nuevo_tamaño+1] = [elemento]
    return lista

print("\n=== Usando mi_append ===")
lista2 = [10, 20]
mi_append(lista2, 30)
print(lista2)  # [10, 20, 30]
