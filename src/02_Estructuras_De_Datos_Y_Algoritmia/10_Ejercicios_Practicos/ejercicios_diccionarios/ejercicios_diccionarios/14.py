def buffer_acumulador(limite):
    """
    BUFFER: acumula hasta 'limite', luego procesa y vacía
    """
    buffer = []
    
    def añadir(elemento):
        nonlocal buffer
        buffer.append(elemento)
        print(f"Añadido {elemento}. Buffer: {len(buffer)}/{limite}")
        
        # ¿Límite alcanzado? PROCESA y VACÍA
        if len(buffer) >= limite:
            print(f"🧹 BUFFER LLENO! Procesando {buffer}...")
            procesar_buffer(buffer)
            buffer.clear()  # Vacía completamente
            print("Buffer vaciado ✅")
    
    def estado():
        return f"Buffer actual: {buffer}"
    
    return añadir, estado

def procesar_buffer(datos):
    """Simula procesamiento (envío batch, escritura disco, etc.)"""
    print(f"  → Procesados {len(datos)} elementos: {sum(datos) if datos else 0}")


# Buffer de tamaño 3
añadir, estado_buffer = buffer_acumulador(limite=3)

print("=== LLENANDO BUFFER ===\n")
añadir(10)  # [10]
añadir(20)  # [10, 20] 
añadir(30)  # [10, 20, 30] → PROCESA!

añadir(40)  # [] → Nuevo ciclo
añadir(50)  # [40, 50]
print("\nEstado:", estado_buffer())
