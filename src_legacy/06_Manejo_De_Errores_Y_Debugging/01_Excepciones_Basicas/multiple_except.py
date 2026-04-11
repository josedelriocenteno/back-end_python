"""
multiple_except.py
=================

Objetivo:
- Aprender a capturar y manejar múltiples tipos de excepciones
- Mantener código limpio y legible
- Evitar bloques except genéricos y confusos
"""

# -------------------------------------------------------------------
# 1️⃣ USO DE MÚLTIPLES EXCEPTS
# -------------------------------------------------------------------

# Ejemplo clásico: dividir dos números y convertir a entero
numeros = ["10", "0", "abc"]

for n in numeros:
    try:
        valor = int(n)
        resultado = 100 / valor
    except ValueError as e:
        # Captura errores de conversión
        print(f"Error de conversión: {e}")
    except ZeroDivisionError as e:
        # Captura división por cero
        print(f"Error de división: {e}")
    else:
        # Se ejecuta si no hubo excepción
        print(f"Resultado = {resultado}")
    finally:
        # Código que siempre se ejecuta
        print(f"Intento con '{n}' completado\n")

# -------------------------------------------------------------------
# 2️⃣ CAPTURAR VARIOS TIPOS EN UN SOLO EXCEPT
# -------------------------------------------------------------------

# Forma concisa: tupla de excepciones
for n in numeros:
    try:
        valor = int(n)
        resultado = 100 / valor
    except (ValueError, ZeroDivisionError) as e:
        print(f"Error capturado: {e}")
    else:
        print(f"Resultado = {resultado}")
    finally:
        print(f"Intento con '{n}' completado\n")

# Nota:
# - Útil si la acción ante varios errores es la misma
# - Mantiene código limpio y evita repetición

# -------------------------------------------------------------------
# 3️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# 1. Captura específica siempre que sea posible
# 2. Usa tuplas solo si la acción a tomar es idéntica
# 3. Evita except genérico salvo logging global
# 4. Usa else para código que solo debe ejecutarse si no hubo excepción
# 5. Usa finally para liberar recursos, cerrar archivos o conexiones

# Ejemplo de combinación correcta:

def procesar_valor(n: str):
    try:
        valor = int(n)
        resultado = 100 / valor
    except ValueError:
        print(f"'{n}' no es un número válido")
    except ZeroDivisionError:
        print("No se puede dividir por cero")
    else:
        print(f"Resultado = {resultado}")
    finally:
        print(f"Intento con '{n}' completado\n")

for n in numeros:
    procesar_valor(n)
