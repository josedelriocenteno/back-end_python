# Paralelismo en Python: Multiprocessing y Asyncio

Python es un lenguaje muy potente, pero su gran limitación de rendimiento es el **GIL (Global Interpreter Lock)**. Aprender a saltárselo es la diferencia entre un script lento y un pipeline de alto rendimiento.

## 1. Multithreading (Hilos)
*   **Qué hace:** Ejecuta tareas en paralelo pero dentro del mismo proceso.
*   **Uso ideal:** Tareas **I/O-bound** (esperar red, leer disco, consultar API).
*   **Límitación:** Debido al GIL, no ofrece ventajas de velocidad para tareas matemáticas o de procesamiento de datos pesadas.

## 2. Multiprocessing (Procesos)
*   **Qué hace:** Crea procesos hijos independientes, cada uno con su propia memoria y su propio intérprete de Python.
*   **Uso ideal:** Tareas **CPU-bound** (procesar imágenes, cálculos matemáticos, transformaciones de datos grandes).
*   **Ventaja:** Salta el GIL y aprovecha todos los núcleos de tu procesador.
*   **Contras:** Consume mucha más RAM y la comunicación entre procesos es más compleja.

## 3. Asyncio (Asincronía)
*   **Qué hace:** Es un "bucle de eventos" (Event Loop) que permite que un solo hilo gestione miles de tareas concurrentes.
*   **Uso ideal:** Servidores web y APIs que consultan bases de datos o servicios externos.
*   **Filosofía:** "No esperes parado". Mientras los datos viajan por la red, `asyncio` permite que el código haga otras cosas.

## 4. Ejemplo rápido: Pool de Procesos
```python
from multiprocessing import Pool

def procesamiento_pesado(dato):
    # Imagina un cálculo complejo aquí
    return dato * dato

if __name__ == "__main__":
    datos = range(1000000)
    # Usamos 4 núcleos para repartir el trabajo
    with Pool(4) as p:
        resultados = p.map(procesamiento_pesado, datos)
```

## 5. El error del "Overhead"
Crear un proceso o un hilo tiene un coste de tiempo. Si tu tarea es muy rápida (ej: sumar dos números), tardarás más tiempo en crear el hilo que en hacer el cálculo. Usa paralelismo solo para tareas que duren al menos unos milisegundos.

## Resumen: La herramienta para cada carga
Usa `asyncio` para que tu API no se bloquee. Usa `multiprocessing` para que tu transformación de datos sea rápida. Dominar la concurrencia en Python es lo que permite escalar procesos locales a niveles industriales.
