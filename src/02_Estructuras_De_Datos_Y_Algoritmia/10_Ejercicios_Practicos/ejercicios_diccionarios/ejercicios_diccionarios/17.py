def agrupar_flexible(datos, tamano=3, metodo="slicing"):
    """Método configurable"""
    if metodo == "lc":
        return [datos[i:i+tamano] for i in range(0, len(datos), tamano)]
    elif metodo == "itertools":
        from itertools import islice
        it = iter(datos)
        return list(iter(lambda: list(islice(it, tamano)), []))
    else:  # slicing manual
        return [datos[i:i+tamano] for i in range(0, len(datos), tamano)]

# USO
print(agrupar_flexible(range(10), tamano=3, metodo="lc"))
