# Complejidad Básica en Backend Python (Big-O de Verdad)

## 1. Por qué esto importa (mucho)

La complejidad **no es teoría académica**, es lo que decide si:
- tu API responde en 50 ms o en 5 segundos
- tu script procesa 10k registros o se muere con 1M
- tu backend escala o se rompe

> Backend lento casi nunca es “Python lento”  
> Es **mala elección de algoritmos y estructuras**.

---

## 2. Qué es la complejidad (sin bullshit)

La complejidad mide:
- **cómo crece el tiempo** de ejecución
- **cómo crece el uso de memoria**
cuando aumenta el tamaño de los datos (`n`)

No mide segundos exactos, mide **tendencia**.

---

## 3. Las complejidades que DEBES conocer

### O(1) – Constante (ideal)
No importa el tamaño del input.

Ejemplos:
- acceso a diccionario por clave
- acceso a set
- acceso a lista por índice

```python
usuario = usuarios[42]
Backend feliz.

O(n) – Lineal (aceptable)
Crece proporcional al número de elementos.

Ejemplos:

recorrer una lista

buscar en una lista

filtrar datos

python
Copiar código
for usuario in usuarios:
    procesar(usuario)
Correcto mientras n no sea enorme.

O(n²) – Cuadrático (peligroso)
Explota muy rápido.

Ejemplo clásico:

python
Copiar código
for a in datos:
    for b in datos:
        comparar(a, b)
Con 10k elementos → 100 millones de operaciones
En backend: NO.

O(log n) – Logarítmico (muy bueno)
Escala genial.

Ejemplo:

búsquedas binarias

índices en bases de datos

No muy común en Python puro, pero clave en SQL.

4. Complejidad real de estructuras básicas
Listas
Operación	Complejidad
append	O(1)
pop() final	O(1)
acceso por índice	O(1)
insert / pop inicio	O(n)
búsqueda in	O(n)

👉 Error típico: usar listas para búsquedas.

Sets
Operación	Complejidad
pertenencia	O(1)
add/remove	O(1)

👉 Perfectos para validaciones y filtros.

Diccionarios
Operación	Complejidad
acceso	O(1)
insertar	O(1)
eliminar	O(1)

👉 Columna vertebral del backend.

5. Ejemplo real: lista vs set
python
Copiar código
ids = list(range(1_000_000))

if 999_999 in ids:
    pass  # O(n)
Solución profesional:

python
Copiar código
ids = set(ids)

if 999_999 in ids:
    pass  # O(1)
Mismo resultado, diferencia brutal de rendimiento.

6. El error más común de principiantes
“Funciona, luego está bien”

NO.

Si no sabes:

cuántos datos tendrás

cómo crecerá el sistema

Estás sembrando deuda técnica.

7. Complejidad y backend real
APIs
loops dentro de loops → peligro

validaciones repetidas → sets

acceso por ID → diccionarios

Data / ETL
cargar todo en memoria → error

usar generadores → correcto

pensar en batches → obligatorio

8. No optimices pronto, pero piensa pronto
Regla profesional:

❌ no micro-optimizaciones

✔️ buenas decisiones estructurales desde el inicio

Elegir bien listas / sets / dicts ya es optimizar.

9. Checklist mental de complejidad
Antes de escribir código pregúntate:

¿cuántos elementos puede haber?

¿esta operación se repite?

¿hay búsquedas frecuentes?

¿estoy recorriendo más de lo necesario?

¿esto escala a 10x? ¿100x?

Si no sabes responder → problema.

10. Regla de oro final
La complejidad no se arregla con hardware,
se arregla con cerebro.

Si dominas esto, ya estás pensando como backend engineer.