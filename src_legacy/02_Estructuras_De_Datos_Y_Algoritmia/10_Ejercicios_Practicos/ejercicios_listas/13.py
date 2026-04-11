def push_manual(lista, elemento):
    """Simula push SIN append()"""
    lista[len(lista):len(lista)+1] = [elemento]

def pop_manual(lista):
    """Simula pop SIN pop()"""
    if len(lista) == 0:
        raise IndexError("Pila vacía")
    ultimo = lista[-1]      # Leer top
    del lista[-1]           # Eliminar top
    return ultimo

# PRUEBA MANUAL
pila_manual = [1, 2, 3]
print("\n=== PUSH/POP MANUAL ===")
push_manual(pila_manual, 99)
print("Push manual:", pila_manual)  # [1, 2, 3, 99]

print("Pop manual:", pop_manual(pila_manual))  # 99
print("Resultado:", pila_manual)               # [1, 2, 3]
