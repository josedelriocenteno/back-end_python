import time

lista_grande = list(range(1000000))  # 1M elementos

# append() - súper rápido
start = time.time()
lista_grande.append(999)
print("append():", time.time() - start, "segundos")  # ~0.000001s

# insert(0, ...) - DESASTROSO
start = time.time()
lista_grande.insert(0, 999)
print("insert(0,...):", time.time() - start, "segundos")  # ~0.1s
