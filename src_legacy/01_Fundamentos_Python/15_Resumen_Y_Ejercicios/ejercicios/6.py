lista = "10,20,30,40"

def convertir_a_enteros(valor):
  return int(valor)


lista_enteros = [convertir_a_enteros(e) for e in lista.split(',')]

print(lista_enteros)