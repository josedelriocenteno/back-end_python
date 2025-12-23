# Buenas Prácticas de Funciones en Backend Python – Nivel Profesional

## 1. Función clara y corta

- Máximo 20–30 líneas idealmente
- Un solo propósito (Single Responsibility Principle)
- Nombre que describe claramente lo que hace

```python
# ❌ Malo: función hace varias cosas
def procesar_usuario(usuario):
    usuario["rol"] = "user"
    print(f"Procesando {usuario}")
    return usuario["rol"]

# ✔️ Profesional: separación de responsabilidades
def asignar_rol(usuario, rol="user"):
    usuario["rol"] = rol
    return usuario

def log_usuario(usuario):
    print(f"Procesando {usuario}")
```
---
## 2. Tipado y hints
Siempre usar type hints en parámetros y retorno

Facilita lectura, detección de errores y autocompletado en IDE

```python
from typing import Dict

def asignar_rol(usuario: Dict[str, str], rol: str = "user") -> str:
    usuario["rol"] = rol
    return usuario["rol"]
```
---
## 3. Parámetros claros
Posicionales para obligatorios

Nombrados (keyword) para opcionales

Evitar mutable como valor por defecto

```python
# ❌ Mutable por defecto
def agregar_item(lista=[]):
    lista.append(1)
    return lista

# ✔️ Correcto
def agregar_item_seguro(lista=None):
    if lista is None:
        lista = []
    lista.append(1)
    return lista
```
---
## 4. Funciones puras siempre que sea posible
Salida depende solo de parámetros

Sin efectos secundarios

Facilita testing y paralelización

```python
Copiar código
def calcular_total(items: list[int]) -> int:
    return sum(items)
```
---
## 5. Documentación y docstrings
Siempre describir qué hace, parámetros y retorno

Facilita lectura, mantenimiento y colaboración

```python
def calcular_promedio(numeros: list[int]) -> float:
    """
    Calcula el promedio de una lista de números.

    Args:
        numeros (list[int]): lista de enteros

    Returns:
        float: promedio de la lista
    """
    return sum(numeros) / len(numeros)
```
---
## 6. Manejo de errores dentro de la función
Validar parámetros

Lanzar excepciones claras

No silenciar errores con pass

```python
def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
```
---
## 7. Evitar side-effects innecesarios
No imprimir dentro de funciones de lógica

Separar cálculo de IO o efectos secundarios

```python
# ❌ Mal
def procesar_usuario(usuario):
    print(f"Procesando {usuario}")
    return usuario["rol"]

# ✔️ Correcto
def procesar_usuario_backend(usuario):
    return usuario["rol"]
```
---
## 8. Reutilización y modularidad
Funciones pequeñas y específicas → más fáciles de reutilizar

Evitar código duplicado

```python
def es_mayor_edad(edad: int) -> bool:
    return edad >= 18

def puede_votar(usuario):
    return es_mayor_edad(usuario["edad"])
```
---
## 9. Checklist mental backend
✔️ Función clara y corta?

✔️ Parámetros y retorno tipados?

✔️ Sin side-effects innecesarios?

✔️ Testable y mantenible?

✔️ Propósito único?

---
## 10. Errores comunes de juniors
Mezclar lógica y print

Mutable por defecto

Funciones largas y multifunción

Falta de docstrings

Retorno inconsistente

---
## 11. Regla de oro
Una función profesional es: clara, corta, tipada, testable y predecible.
Todo lo demás genera deuda técnica.

---

🔥 **Verdad profesional**  
Si tus funciones no cumplen estas reglas, **tu backend se vuelve inmanejable antes de escalar**.  