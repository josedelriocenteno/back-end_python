# debugging_en_vscode.md
========================

Objetivo:
---------
Aprender a usar **el debugger visual de VSCode** de manera profesional para inspeccionar el flujo de Python, detectar errores y optimizar el desarrollo sin saturar la consola.

---

## 1️⃣ CONFIGURACIÓN INICIAL

1. Instalar la extensión **Python** de Microsoft en VSCode.
2. Seleccionar el **intérprete de Python correcto** (Python 3.7+ recomendado).
3. Crear un archivo `launch.json` si es necesario:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Archivo Actual",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}

    Guardar y recargar VSCode para que reconozca la configuración.

2️⃣ BREAKPOINTS VISUALES

    Colocar breakpoints haciendo click en la margen izquierda del editor.

    Tipos de breakpoints:

        Normales: Se detienen siempre en la línea.

        Condicionales: Se detienen solo si se cumple una condición.

        Logpoints: En lugar de detener, imprimen un mensaje en la consola.

Ejemplo:

x = 10
y = 0
resultado = x / y  # 🔴 Breakpoint normal

    En ejecución, VSCode se detendrá aquí y permitirá inspección.

3️⃣ INSPECCIÓN DE VARIABLES

    Panel “Variables” muestra:

        Variables locales

        Variables globales

        Objetos complejos

    Permite expandir diccionarios, listas y objetos.

    Visualiza el tipo y valor en tiempo real.

4️⃣ WATCHES Y EXPRESIONES

    Panel “Watch” permite monitorear expresiones específicas.

    Ejemplo:

        x / (y+1) → se recalcula automáticamente al avanzar paso a paso.

    Útil para depurar fórmulas o condiciones críticas.

5️⃣ CALL STACK

    Panel “Call Stack” muestra la secuencia de funciones que llevaron al punto actual.

    Permite:

        Navegar a cualquier nivel de la pila

        Entender el flujo exacto de llamadas

        Detectar dónde ocurre realmente la excepción

6️⃣ PASO A PASO

    Step Over (F10): Ejecuta línea actual y pasa a la siguiente sin entrar en funciones llamadas.

    Step Into (F11): Entra en la función llamada.

    Step Out (Shift+F11): Sale de la función actual.

    Continue (F5): Continúa hasta el siguiente breakpoint.

7️⃣ BUENAS PRÁCTICAS PROFESIONALES

    Usar breakpoints condicionales para bucles grandes o datos específicos.

    Registrar contexto en logs antes de depurar remotamente.

    No depender únicamente de print; usar watch y variables del debugger.

    Combinar con testing y logging para fail-fast.

    Mantener el código limpio; eliminar breakpoints antes de commits a producción.

8️⃣ EJEMPLO PRÁCTICO

Supongamos un flujo de cálculo de promedio:

def calcular_promedio(lista):
    if not lista:
        return 0
    total = sum(lista)
    promedio = total / len(lista)
    return promedio

valores = [10, 20, 30, 40]
prom = calcular_promedio(valores)  # Colocar breakpoint aquí
print("Promedio:", prom)

    Coloca breakpoint en la línea prom = ...

    Usa Step Into para entrar en calcular_promedio()

    Observa variables lista, total, promedio en panel Variables

    Añade un watch para promedio y verifica el cálculo

✅ Resumen

    VSCode debugger es profesional, visual e interactivo.

    Breakpoints, watch, call stack y step permiten inspección total del flujo.

    Siempre combinar con logging y tests; no depender solo de debugger.

    El objetivo es identificar errores rápido y mantener código limpio y seguro.