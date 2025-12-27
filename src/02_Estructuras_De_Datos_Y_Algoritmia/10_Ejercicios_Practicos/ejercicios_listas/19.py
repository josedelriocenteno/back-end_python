# 🎯 Listas son MUTABLES → Modificaciones AFECTAN la original

def modificar_original(lista):
    """Modifica lista IN-PLACE → afecta original"""
    lista.append(999)           # ✅ MUTA el objeto
    lista[0] = "MODIFICADO"     # ✅ Cambia elemento
    lista.extend([100, 200])    # ✅ Añade múltiples

# PRUEBA
mi_lista = [1, 2, 3]
print("ANTES:", mi_lista)

modificar_original(mi_lista)
print("DESPUÉS:", mi_lista)  # [MODIFICADO, 2, 3, 999, 100, 200]

print("ID MISMO:", id(mi_lista))  # ← ¡Mismo objeto en memoria!
