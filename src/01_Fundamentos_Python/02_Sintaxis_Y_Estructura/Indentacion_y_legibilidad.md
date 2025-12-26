# Indentación y Legibilidad en Python

## 1. Introducción

La **indentación y legibilidad** son pilares fundamentales en Python.  
A diferencia de otros lenguajes, Python **utiliza la indentación para definir bloques de código**, no llaves `{}`.  
Escribir código limpio y bien indentado es esencial para **evitar errores, facilitar mantenimiento y colaborar profesionalmente**.

> ⚠️ Nota:  
> La legibilidad en Python no es opcional; sigue las **PEP8 y Zen de Python**, adoptando buenas prácticas desde el primer día.

---

## 2. Indentación correcta

### 2.1 Uso de espacios vs tabulaciones

- Se recomienda **4 espacios por nivel de indentación**.  
- No mezclar tabs y espacios, esto provoca errores de ejecución difíciles de detectar.

```python
# Correcto
if True:
    print("Indentación con 4 espacios")

# Incorrecto
if True:
	print("Tabulador en lugar de espacios")
2.2 Niveles de indentación
Evitar más de 3 niveles de indentación en un mismo bloque.

Dividir lógica compleja en funciones auxiliares para mantener legibilidad.

python
Copiar código
# Demasiados niveles: difícil de leer
if a > 0:
    if b > 0:
        if c > 0:
            print("Tres niveles anidados")

# Pythonic: dividir en función
def check_positive(a, b, c):
    return all(x > 0 for x in (a, b, c))

if check_positive(a, b, c):
    print("Todos positivos")
3. Legibilidad del código
3.1 Nombres descriptivos
Variables, funciones y clases deben expresar su propósito.

python
Copiar código
# Malo
def f(x):
    return x**2

# Bueno
def calcular_cuadrado(numero):
    return numero**2
3.2 Evitar líneas demasiado largas
Máximo recomendado: 79 caracteres por línea (PEP8).

Usar saltos de línea y paréntesis para mejorar lectura.

python
Copiar código
# Malo
resultado = funcion_compleja(param1, param2, param3, param4, param5)

# Bueno
resultado = funcion_compleja(
    param1,
    param2,
    param3,
    param4,
    param5
)
3.3 Espacios y separadores
Añadir espacios después de comas, operadores y alinear asignaciones para claridad.

python
Copiar código
# Correcto
x = 10
y = 20
resultado = x + y

# Incorrecto
x=10
y=20
resultado=x+y
4. Uso de comentarios y docstrings
Comentarios: explicar “por qué” se hace algo, no “qué hace” el código.

Docstrings: documentar funciones, clases y módulos.

python
Copiar código
def calcular_area(base: float, altura: float) -> float:
    """
    Calcula el área de un rectángulo.
    
    Args:
        base (float): Base del rectángulo
        altura (float): Altura del rectángulo
    
    Returns:
        float: Área calculada
    """
    return base * altura
5. Checklist rápido de indentación y legibilidad
 Usar 4 espacios por nivel de indentación

 Evitar mezclar tabs y espacios

 Mantener máximo 3 niveles de indentación por bloque

 Nombres descriptivos para variables, funciones y clases

 Líneas ≤ 79 caracteres, usar saltos de línea cuando sea necesario

 Espacios adecuados alrededor de operadores y comas

 Comentarios claros explicando “por qué”

 Docstrings completos en funciones, clases y módulos

6. Conclusión
La indentación y legibilidad no son solo estética: son críticas para escribir código Python profesional.
Un código bien indentado y legible reduce errores, facilita mantenimiento y permite colaborar eficazmente en proyectos reales de backend, data e IA.