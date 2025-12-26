# Ejercicios de Práctica – Fundamentos Python (Unidad 01)

## Sintaxis y Estructura
1. Escribe un script que reciba argumentos de línea de comandos y los imprima en orden inverso.
2. Crea un módulo que contenga funciones de validación de datos y úsalas desde otro script.
3. Haz un programa que valide si un archivo `.txt` existe y, si no, lo cree.
4. Escribe docstrings para todas tus funciones y clases de un proyecto pequeño.

## Tipos de Datos y Conversiones
5. Convierte una lista de strings `["1", "2.5", "True", "None"]` a sus tipos correctos (`int`, `float`, `bool`, `NoneType`).
6. Dado un string con formato `"10,20,30,40"`, conviértelo en una lista de enteros.
7. Escribe un script que detecte automáticamente el tipo de cada elemento en una lista y lo convierta a un tipo estándar.
8. Practica conversiones de float a int y viceversa en cálculos de precios con redondeo profesional.

## Estructuras de Datos
9. Dada una lista de usuarios con diccionarios `{id, nombre, edad}`, crea:
   - Un diccionario por `id`
   - Una lista de nombres
   - Un set con edades únicas
10. Dadas dos listas grandes de números, encuentra elementos comunes usando sets y comprueba eficiencia.
11. Crea una función que reciba una lista y devuelva un diccionario con la frecuencia de cada elemento.
12. Implementa una cola (FIFO) y un stack (LIFO) usando `deque` y haz operaciones de prueba.

## Control de Flujo
13. Escribe un programa que clasifique números en positivos, negativos y ceros.
14. Haz un bucle que sume números hasta alcanzar un límite dado, usando `while`.
15. Crea un script que procese una lista y use `break`, `continue` y `pass` correctamente.
16. Simula un menú interactivo con `if-elif-else` y bucles hasta que el usuario decida salir.

## Funciones
17. Escribe una función que reciba cualquier número de parámetros y devuelva su suma y promedio.
18. Crea funciones puras que transformen listas sin modificar la original.
19. Implementa una función que reciba otra función como argumento y la aplique a una lista de datos.
20. Diseña funciones con argumentos posicionales, nominales y por defecto, y prueba combinaciones.

## Manejo de Errores
21. Crea una función que lea números de un archivo, ignore los inválidos y devuelva la suma.
22. Simula errores comunes (ZeroDivisionError, IndexError, KeyError) y maneja cada uno de manera profesional.
23. Implementa un sistema de logging para registrar errores capturados en un diccionario.
24. Haz un script que intente conectarse a un recurso (ficticio) y use `try-except-else-finally`.

## Módulos y Paquetes
25. Crea un paquete `utils` con funciones de validación y transformación de datos, e imprótalo en varios scripts.
26. Crea un módulo con constantes y úsalo en funciones de cálculo.
27. Experimenta con `from module import *` vs import explícito y observa diferencias de namespace.

## Input / Output
28. Escribe un programa que lea un CSV de ventas y calcule totales por producto.
29. Crea un script que escriba logs en un archivo `.log` con timestamps.
30. Practica rutas absolutas y relativas con `os.path` y `Pathlib`.
31. Lee un archivo grande línea a línea sin cargar todo en memoria y cuenta ocurrencias de palabras.

## Strings Avanzados
32. Formatea un reporte usando f-strings y alineación de columnas.
33. Dado un texto, cuenta vocales y consonantes usando comprehensions.
34. Extrae todos los números de un string y conviértelos en enteros.
35. Crea un sistema de plantillas con f-strings que genere emails personalizados.

## Iterables y Comprehensions
36. Genera listas, sets y diccionarios con comprehensions para datos de ejemplo.
37. Filtra elementos de una lista según múltiples condiciones usando comprehensions.
38. Combina `zip` y comprehensions para crear un diccionario a partir de dos listas.
39. Practica nested comprehensions con matrices 2D.

## Funciones Built-in
40. Usa `map`, `filter` y `zip` para procesar datos de usuarios y obtener resultados agregados.
41. Usa `any` y `all` para validar datos de forma profesional.
42. Usa `sum`, `min` y `max` en un dataset de precios simulando pipelines de datos.

## Complejidad y Rendimiento
43. Compara tiempo de ejecución entre:
   - Listas vs sets para membership test
   - Nested loops vs diccionarios para búsqueda
44. Genera listas grandes y mide rendimiento de operaciones con `time` o `timeit`.
45. Refactoriza código O(n^2) usando estructuras más eficientes.

## Buenas Prácticas
46. Refactoriza un script largo en funciones pequeñas y módulos.
47. Aplica PEP8 con linters y formatters.
48. Documenta un mini proyecto con docstrings y README.
49. Crea tests simples para funciones críticas usando asserts.
50. Revisa código antiguo y detecta posibles mejoras de legibilidad, modularidad y eficiencia.
