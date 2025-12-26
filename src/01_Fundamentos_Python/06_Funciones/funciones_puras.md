# Funciones Puras en Backend Python – Nivel Profesional

## 1. Qué es una función pura

Una función pura cumple dos reglas:

1. Su salida depende **solo de los parámetros que recibe**.
2. No produce **efectos secundarios** (no modifica variables externas, no escribe en archivos, no hace print, no hace llamadas a la red).

> Las funciones puras son **predecibles y fáciles de testear**.

---

## 2. Por qué importan en backend

- Evitan bugs silenciosos
- Facilitan testing unitario
- Permiten paralelización y caching
- Mantienen lógica separada de efectos

---

## 3. Ejemplo de función pura

```python
def sumar(a: int, b: int) -> int:
    return a + b
```
>Entrada: a, b

>Salida: suma

Ningún efecto secundario

---
## 4. Ejemplo de función impura
```python 
contador_global = 0

def incrementar():
    global contador_global
    contador_global += 1
```
Modifica estado externo → impura

Difícil de testear y causa bugs silenciosos

---

## 5. Funciones puras con colecciones
```python
def duplicar_lista(lista):
    return [x * 2 for x in lista]
```
La lista original no se modifica

Salida depende solo del input

❌ No hacer:

```python
def duplicar_lista_mala(lista):
    for i in range(len(lista)):
        lista[i] *= 2  # efecto secundario
    return lista
```
---
## 6. Funciones puras y datos complejos
Evitar modificar diccionarios o objetos mutables pasados como argumentos

Si necesitas cambiar algo → devolver copia

```python
def actualizar_usuario(usuario, nuevo_rol):
    nuevo_usuario = usuario.copy()
    nuevo_usuario["rol"] = nuevo_rol
    return nuevo_usuario
```
---
## 7. Funciones puras y testing
Siempre fáciles de testear con pytest o unit tests

No necesitan mocks de IO

Resultado predecible → tests fiables

## 8. Funciones puras y rendimiento
Permiten memoization / caching

Permiten procesamiento concurrente seguro

Reducen errores de estado compartido

## 9. Patrón profesional
Separar lógica de efectos secundarios

Toda función que devuelve algo → pura

Funciones que hacen side-effects → explícitas y limitadas

```python
Copiar código
# lógica pura
def calcular_total(items):
    return sum(items)

# side-effect controlado
def guardar_total(total):
    with open("total.txt", "w") as f:
        f.write(str(total))
```
---
## 10. Errores comunes de juniors
1. Mezclar print con lógica

2. Modificar parámetros mutables sin copia

3. Dependencia de variables globales

4. Funciones largas (>50 líneas) que hacen todo

---
## 11. Checklist mental backend
✔️ Depende solo de parámetros?

✔️ Sin efectos secundarios?

✔️ Fácil de testear?

✔️ Reutilizable y predecible?

✔️ Corto y conciso?

## 12. Regla de oro
Una función pura es como un bloque Lego: predecible, confiable y fácil de combinar.

---

🔥 **Verdad profesional**  
Backend limpio no es solo “funciona”, es **predecible, testable y escalable**.  
Funciones puras son la base de eso.  