# Estilo de Código Profesional en Python

## 1. Introducción

El **estilo de código profesional** en Python no solo hace que el código sea legible, sino que también garantiza **mantenibilidad, consistencia y colaboración efectiva** en proyectos reales de backend, data e IA.  
Seguir un estilo coherente desde el inicio es **crucial para evitar deuda técnica** y facilitar la revisión de código.

> ⚠️ Nota:  
> La comunidad Python tiene estándares bien definidos (PEP8 y PEP257) que todo profesional debe seguir.

---

## 2. Principios de estilo profesional

1. **Legibilidad primero**  
   - Código fácil de leer y entender.  
   - Evitar “trucos” complejos que solo el autor comprende.

2. **Consistencia**  
   - Nombres, espacios, indentación y formato uniforme en todo el proyecto.

3. **Modularidad**  
   - Dividir en funciones, clases y módulos claros con responsabilidad única.

4. **Documentación clara**  
   - Docstrings completos y comentarios que expliquen “por qué”, no “qué”.

5. **Evitar código duplicado**  
   - Reutilizar funciones y módulos, no copiar-pegar lógica.

---

## 3. Convenciones PEP8 clave

### 3.1 Nombres

| Tipo | Convención | Ejemplo |
|------|-----------|---------|
| Variables y funciones | snake_case | `calcular_area` |
| Clases | PascalCase | `Rectangulo` |
| Constantes | UPPER_CASE | `PI = 3.1416` |
| Módulos | snake_case | `modulo_utilidades.py` |
| Paquetes | snake_case | `data_engineering` |

### 3.2 Indentación y líneas

- 4 espacios por nivel, no mezclar tabs.  
- Máximo 79 caracteres por línea.  
- Líneas en blanco para separar funciones, clases y bloques lógicos.

```python
# Correcto
def procesar_datos(datos):
    resultado = []
    for dato in datos:
        resultado.append(dato*2)
    return resultado
3.3 Espacios
Espacios después de comas y operadores.

Evitar espacios innecesarios en paréntesis y llamadas a funciones.

python
Copiar código
# Correcto
x = 10 + 5
funcion(a, b, c)

# Incorrecto
x=10+5
funcion( a,b ,c )
4. Docstrings y comentarios
Cada función y clase debe tener docstring descriptivo.

Los comentarios deben explicar la intención o decisión de diseño, no lo obvio.

python
Copiar código
def calcular_promedio(lista: list) -> float:
    """
    Calcula el promedio de una lista de números.

    Args:
        lista (list): Lista de números (int o float)

    Returns:
        float: Promedio calculado
    """
    return sum(lista) / len(lista)
5. Organización del proyecto
Estructura modular y clara:

css
Copiar código
proyecto/
├── main.py
├── modules/
│   ├── procesamiento.py
│   └── utils.py
├── tests/
│   ├── test_procesamiento.py
│   └── test_utils.py
└── requirements.txt
Separar lógica de negocio, utilidades y scripts de ejecución.

Mantener nombres descriptivos y consistentes.

6. Checklist rápido de estilo profesional
 Seguir PEP8: indentación, longitud de línea y espacios

 Nombres consistentes y descriptivos

 Funciones y clases pequeñas y con responsabilidad única

 Docstrings claros con parámetros, retornos y excepciones

 Evitar código duplicado y “trucos” complicados

 Estructura modular y directorios organizados

 Comentarios útiles explicando “por qué”

 Mantener consistencia en todo el proyecto

7. Conclusión
Seguir un estilo de código profesional asegura que tu proyecto sea legible, mantenible y escalable, facilitando la colaboración en equipos y la entrega de software de calidad.
Adoptar estas prácticas desde el inicio te posiciona como un desarrollador backend, data o IA profesional.