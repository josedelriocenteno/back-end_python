# Lista anidada original
lista_original = [[1, 2], [3, 4], [5, 6]]

# REFERENCIA a la misma lista (no copia)
ref1 = lista_original
# COPIA SUPERFICIAL (solo copia la lista exterior)
ref2 = lista_original.copy()
# COPIA SUPERFICIAL con slicing
ref3 = lista_original[:]

print("=== ANTES de modificar ===")
print("Original:", lista_original)
print("ref1:", ref1)
print("ref2:", ref2)
print("ref3:", ref3)

# MODIFICAMOS la lista anidada (elemento interior)
lista_original[0].append(99)  # Cambia el primer sublista: [1, 2, 99]

print("\n=== DESPUÉS de lista_original[0].append(99) ===")
print("Original:", lista_original)  # ← CAMBIÓ
print("ref1:", ref1)              # ← CAMBIÓ (misma referencia)
print("ref2:", ref2)              # ← CAMBIÓ (copia superficial)
print("ref3:", ref3)              # ← CAMBIÓ (copia superficial)

# AHORA modificamos la lista EXTERIOR
lista_original.append([7, 8])     # Añade nueva sublista

print("\n=== DESPUÉS de lista_original.append([7,8]) ===")
print("Original:", lista_original)  # ← [ [1,2,99], [3,4], [5,6], [7,8] ]
print("ref1:", ref1)               # ← CAMBIÓ (misma referencia)
print("ref2:", ref2)               # ← NO cambió (copia independiente)
print("ref3:", ref3)               # ← NO cambió (copia independiente)
