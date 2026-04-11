def enqueue(lista, elemento):
    """AÑADIR al FINAL - O(1)"""
    lista.append(elemento)

def dequeue(lista):
    """ELIMINAR del INICIO - O(n) ⚠️"""
    if len(lista) == 0:
        raise IndexError("Cola vacía")
    return lista.pop(0)  # ← PROBLEMA: O(n)

# PRUEBA COLA FIFO (First In, First Out)
cola = []

print("=== ENQUEUE ===")
enqueue(cola, 10)  # [10]
enqueue(cola, 20)  # [10, 20]
enqueue(cola, 30)  # [10, 20, 30]
print("Cola:", cola)

print("\n=== DEQUEUE ===")
print("Dequeue:", dequeue(cola))  # 10 (primero)
print("Cola:", cola)              # [20, 30]
