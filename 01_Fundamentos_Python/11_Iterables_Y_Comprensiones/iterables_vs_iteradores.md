# Iterables vs Iteradores en Python – Backend Profesional

## 1. Concepto clave

- **Iterable:** objeto que puede ser recorrido en un bucle `for`.  
  Ejemplos: list, tuple, dict, set, str.  
  - Tiene el método `__iter__()`.
  - Cada llamada a `iter()` devuelve un **iterador**.

- **Iterador:** objeto que produce elementos uno a uno bajo demanda.  
  - Tiene los métodos `__iter__()` y `__next__()`.
  - Se usa para **procesar grandes volúmenes de datos sin cargarlos todos en memoria**.

---

## 2. Diferencia práctica

```python
# Iterable
mi_lista = [1, 2, 3, 4]
for elemento in mi_lista:
    print(elemento)

# Iterador
mi_iterador = iter(mi_lista)
print(next(mi_iterador))  # 1
print(next(mi_iterador))  # 2
Cada iterable puede generar múltiples iteradores independientes.

Los iteradores consumen sus elementos: una vez recorridos, no se pueden reutilizar sin crear uno nuevo.

3. Uso profesional en backend
Evitar cargar grandes datasets completos en memoria.

Procesar logs o streams línea por línea.

python
Copiar código
def leer_archivo_grande(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:  # f es iterable, produce iterador internamente
            yield linea.strip()  # Generador = iterador bajo demanda
yield transforma la función en un generador, que es un iterador eficiente.

4. Iteradores vs listas: eficiencia
python
Copiar código
# Lista completa (carga toda en memoria)
numeros = [x**2 for x in range(10_000_000)]

# Iterador con generador (lazy evaluation)
numeros_iter = (x**2 for x in range(10_000_000))

# Solo se calculan los valores cuando se necesitan
✔️ Generadores = bajo consumo de memoria, ideales para pipelines de datos y streams.

5. Comportamiento en bucles
python
Copiar código
mi_iter = iter([1,2,3])
for x in mi_iter:
    print(x)  # 1,2,3

for x in mi_iter:
    print(x)  # No imprime nada, el iterador ya se consumió
Los iteradores no son reiniciables.

Para reiniciar, crear un nuevo iterador desde el iterable.

6. Errores comunes de juniors
❌ Intentar iterar varias veces sobre un iterador sin recrearlo

❌ Cargar datasets enormes en listas innecesariamente

❌ Confundir iterable con iterador

❌ No usar yield para procesamiento lazy → alto consumo de memoria

7. Buenas prácticas profesionales
Usar iterables cuando necesitas múltiples pasadas sobre los datos.

Usar iteradores/generadores para procesamiento bajo demanda y streaming.

Evitar cargar toda la data en memoria si no es necesario.

Documentar cuándo un objeto es iterable y cuándo iterador.

Aprovechar enumerate(), zip(), map() y filter() para loops limpios y eficientes.

8. Checklist mental backend
✔️ Iterable o iterador correctamente usado?

✔️ Procesamiento lazy cuando es necesario?

✔️ Memoria optimizada en datasets grandes?

✔️ Código limpio y profesional para loops?

9. Regla de oro
En backend y pipelines, procesa los datos bajo demanda siempre que sea posible.
Los iteradores y generadores son la clave para eficiencia y escalabilidad profesional.

yaml
Copiar código

---

🔥 **Verdad profesional**  
El 60% de problemas de memoria en pipelines de datos provienen de **usar listas completas en lugar de iteradores/generadores**.