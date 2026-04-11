# 🚨 PROBLEMA: Lista mutable como valor por DEFECTO se COMPARTE

def funcion_peligrosa(numeros=[]):  # ❌ UNA SOLA lista compartida
    numeros.append(999)
    return numeros

# PRUEBA DESASTROSA
print("1ra llamada:", funcion_peligrosa())  # [999]
print("2da llamada:", funcion_peligrosa())  # [999, 999]  ← ¡¿QUÉ?!
print("3ra llamada:", funcion_peligrosa())  # [999, 999, 999] 😱
