# Big O y Notación de Complejidad – Backend Profesional

## 1. Qué es la Notación Big O

- La notación **Big O** describe **cómo crece el tiempo de ejecución o el uso de memoria de un algoritmo** según el tamaño de la entrada.
- Es fundamental para **backend y pipelines de datos** donde los volúmenes pueden ser enormes.
- Permite **predecir cuellos de botella** y elegir algoritmos eficientes.

---

## 2. Conceptos básicos

- **O(1) – Tiempo constante**
  - No importa el tamaño de la entrada, el tiempo de ejecución permanece igual.
  - Ejemplo: acceder a un elemento de un arreglo por índice.
  
- **O(n) – Tiempo lineal**
  - El tiempo crece proporcionalmente al tamaño de la entrada.
  - Ejemplo: recorrer una lista con un bucle `for`.

- **O(n^2) – Tiempo cuadrático**
  - Dos bucles anidados sobre la entrada.
  - Ejemplo: comparaciones de todos contra todos en un array.

- **O(log n) – Tiempo logarítmico**
  - Divides el problema en partes y reduces la búsqueda.
  - Ejemplo: búsqueda binaria en una lista ordenada.

- **O(n log n) – Tiempo lineal-logarítmico**
  - Algoritmos de ordenamiento eficientes (merge sort, quicksort promedio).

---

## 3. Ejemplos en Python

```python
# O(1) – Acceso a índice
numeros = [1,2,3,4,5]
print(numeros[2])

# O(n) – Recorrer lista
for n in numeros:
    print(n)

# O(n^2) – Nested loop
for i in numeros:
    for j in numeros:
        print(i,j)

# O(log n) – Búsqueda binaria
def busqueda_binaria(lista, objetivo):
    izquierda, derecha = 0, len(lista)-1
    while izquierda <= derecha:
        medio = (izquierda+derecha)//2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            izquierda = medio+1
        else:
            derecha = medio-1
    return -1
4. Coste de memoria (Espacio)
Big O no solo mide tiempo, también memoria.

Ejemplo:

Crear una lista con n elementos → O(n) espacio.

Usar generadores → O(1) espacio adicional.

5. Errores comunes de juniors
Ignorar complejidad al procesar grandes volúmenes de datos.

Usar bucles anidados innecesarios (O(n^2)) cuando se puede usar diccionarios (O(1) lookup).

Mezclar operaciones costosas dentro de loops.

No pensar en espacio → memoria insuficiente en pipelines grandes.

6. Buenas prácticas profesionales
Analiza complejidad antes de escribir código.

Prefiere algoritmos lineales o logarítmicos para datos grandes.

Usa diccionarios y sets para búsquedas rápidas.

Evita nested loops innecesarios.

Usa generadores para reducir consumo de memoria.

Documenta decisiones si elegiste un algoritmo más lento por claridad.

7. Checklist mental backend
✔️ ¿Conozco la complejidad de mis funciones críticas?

✔️ ¿Evité nested loops innecesarios?

✔️ ¿Uso estructuras de datos eficientes (set, dict, heap)?

✔️ ¿Consideré memoria y tiempo para datasets grandes?

8. Regla de oro
En backend profesional:

La eficiencia importa incluso antes de optimizar el código.

Algoritmos ineficientes = pipelines lentos, APIs lentas y problemas de escalabilidad.

Big O es tu guía para escribir código robusto, escalable y profesional.