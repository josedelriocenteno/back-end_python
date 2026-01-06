# errores_vs_excepciones.md
===========================

## Objetivo
- Entender la diferencia entre **errores** y **excepciones**
- Conocer cuándo y cómo manejarlos profesionalmente
- Evitar confundir conceptos al escribir código robusto

---

## 1️⃣ ERRORES (Errors)

- Son problemas graves o fallos que Python detecta durante la ejecución.
- Algunos **no pueden ser recuperados** y usualmente terminan el programa.
- Se dividen principalmente en:
  - **SyntaxError**: error de sintaxis que impide ejecutar el código.
  - **RuntimeError**: error durante la ejecución, como división por cero o acceso a índice inexistente.
  - **LogicalError**: error de lógica del programador, que produce resultados incorrectos sin detener el programa.

**Ejemplo:**

```python
# SyntaxError
# def funcion()  # ❌ falta ':'

# RuntimeError
x = 10
y = 0
# print(x / y)  # ❌ ZeroDivisionError

# LogicalError
notas = [8, 9, 10]
promedio = sum(notas) / 2  # ❌ Error lógico, debería ser len(notas)

Resumen:

    Los errores indican que algo está mal en el código o los datos

    Algunos se pueden capturar, otros son fatales

    Detectarlos a tiempo evita fallos en producción

2️⃣ EXCEPCIONES (Exceptions)

    Son objetos que Python lanza cuando ocurre un error manejable.

    Permiten interrumpir la ejecución normal, manejar el problema y continuar.

    Excepciones son parte del flujo de control del programa, no necesariamente fatales.

    Python tiene excepciones integradas (ZeroDivisionError, FileNotFoundError) y permite crear excepciones personalizadas.

Ejemplo:

try:
    resultado = 10 / 0
except ZeroDivisionError:
    resultado = 0  # Manejo de excepción
print(resultado)  # Output: 0

Ventajas de usar excepciones:

    Código más robusto y seguro

    Evita que el programa se caiga por errores previsibles

    Permite mensajes claros al usuario o logs para debugging

    Facilita separar lógica de manejo de errores

3️⃣ DIFERENCIAS CLAVE
Característica	Error	Excepción
Definición	Problema en el código o datos	Objeto que indica un fallo manejable
Ejemplo	SyntaxError, LogicalError	ZeroDivisionError, FileNotFoundError
Recuperable	No siempre	Sí, mediante try/except
Impacto en ejecución	Puede detener el programa	Se puede manejar y continuar
Creación personal	No se crean	Sí, se pueden definir clases propias
4️⃣ BUENAS PRÁCTICAS

    No confundir errores lógicos con excepciones.

        Un error lógico requiere refactorización o tests.

        Una excepción permite manejar un fallo esperado.

    Captura específica de excepciones.

        Nunca usar except: genérico sin criterio.

    Registrar y loguear información útil.

        Para debugging profesional y reproducibilidad.

    No usar excepciones para controlar flujo normal.

        Excepciones deben ser eventos excepcionales, no la norma.

5️⃣ CONCLUSIÓN

    Errores: problemas que pueden detener tu código o producir resultados incorrectos.

    Excepciones: mecanismos de Python para manejar fallos previsibles y continuar la ejecución.

    Entender la diferencia es clave para diseñar sistemas robustos, estables y mantenibles.