"""
pdb_basico.py
==============

Objetivo:
- Aprender a usar el debugger nativo de Python (`pdb`)
- Inspeccionar variables y flujo paso a paso
- Detectar errores sin saturar la consola ni depender de print
"""

# -------------------------------------------------------------------
# 1️⃣ IMPORTAR Y ACTIVAR PDB
# -------------------------------------------------------------------

# Python tiene un debugger nativo llamado `pdb`
import pdb

def dividir(a, b):
    return a / b

def procesar_valores(x, y):
    resultado = dividir(x, y)
    return resultado + 10

# -------------------------------------------------------------------
# 2️⃣ SETEAR UN BREAKPOINT
# -------------------------------------------------------------------

# Antes de ejecutar una línea problemática
# Colocamos:
# pdb.set_trace()
# El programa se detendrá y permitirá inspección interactiva

def main():
    x = 10
    y = 0

    pdb.set_trace()  # ⬅ Aquí se detendrá la ejecución
    # Dentro del prompt interactivo podemos:
    # - inspeccionar variables: print(x), print(y)
    # - avanzar paso a paso: n (next)
    # - entrar en funciones: s (step)
    # - continuar ejecución: c (continue)

    resultado = procesar_valores(x, y)
    print("Resultado:", resultado)

if __name__ == "__main__":
    main()

# -------------------------------------------------------------------
# 3️⃣ COMANDOS BÁSICOS DE PDB
# -------------------------------------------------------------------

# n : next → ejecuta siguiente línea
# s : step → entra en la función llamada
# c : continue → continúa hasta próximo breakpoint
# l : list → muestra líneas alrededor del punto actual
# p variable → imprime el valor de la variable
# q : quit → salir del debugger

# Ejemplo práctico:
# 1. Se detiene en pdb.set_trace()
# 2. Escribimos 'p x' → muestra 10
# 3. Escribimos 'p y' → muestra 0
# 4. Escribimos 'n' → avanza a procesar_valores()
# 5. Si ocurre ZeroDivisionError, el debugger lo mostrará con traceback

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1. Usar pdb solo en desarrollo o debugging local
# 2. Nunca dejar breakpoints en código de producción
# 3. Combinar con logging para analizar errores de manera persistente
# 4. Usar para inspeccionar variables complejas, loops, funciones recursivas
# 5. Complementar con tests y asserts para fail-fast

# -------------------------------------------------------------------
# 5️⃣ CONSEJO EXTRA
# -------------------------------------------------------------------

# En Python 3.7+ también se puede usar:
# breakpoint()  # ⬅ reemplaza pdb.set_trace()
# Funciona igual, pero respeta la configuración de PYTHONBREAKPOINT
