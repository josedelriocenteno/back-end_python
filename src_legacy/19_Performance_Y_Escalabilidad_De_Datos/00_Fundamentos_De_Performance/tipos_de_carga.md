# Tipos de Carga: CPU-bound vs. I/O-bound

Para optimizar un sistema, primero debes saber qué es lo que lo está frenando. Hay dos tipos principales de límites o "cuellos de botella".

## 1. CPU-bound (Limitado por Cómputo)
El programa va lento porque el procesador está trabajando al 100%.
*   **Ejemplos:**
    *   Cifrado y descifrado de datos.
    *   Compresión de archivos pesados.
    *   Cálculos matemáticos complejos (Machine Learning, simulaciones).
    *   Parseo masivo de JSON o XML complejos en Python.
*   **Solución:**
    *   Algoritmos más eficientes.
    *   Paralelismo (usar todos los núcleos de la CPU).
    *   Mover la lógica a lenguajes más rápidos (C++, Rust) o usar librerías optimizadas (NumPy).

## 2. I/O-bound (Limitado por Entrada/Salida)
El programa va lento porque está esperando a que los datos lleguen del disco o de la red. La CPU suele estar casi parada (ociosa).
*   **Ejemplos:**
    *   Consultas a una base de datos lenta.
    *   Descargar archivos de Internet o de Cloud Storage.
    *   Escribir logs en disco.
    *   Llamadas a APIs externas.
*   **Solución:**
    *   Asincronía (`asyncio` en Python).
    *   Caching (Redis) para evitar repetir lecturas.
    *   Mejorar la red o el almacenamiento (SSD vs HDD).
    *   Batching (agrupar peticiones para reducir el overhead).

## 3. ¿Cómo identificarlo?
*   **Mira el Monitor de Sistema:**
    *   ¿CPU al 100%? -> Eres **CPU-bound**.
    *   ¿CPU al 5% pero el proceso sigue tardando mucho? -> Eres **I/O-bound**.
*   **Usa Profilers:** Herramientas que miden dónde pasa el tiempo el código (ej: `py-spy` o `cProfile` en Python).

## 4. El caso de Python (GIL)
En Python, el **GIL (Global Interpreter Lock)** impide que el código corra en varios núcleos a la vez de forma sencilla para tareas CPU-bound. 
*   Para tareas **CPU-bound** en Python usamos `multiprocessing`.
*   Para tareas **I/O-bound** en Python usamos `threading` o `asyncio`.

## Resumen: Ataca la causa raíz
No compres una CPU de 64 núcleos si tu pipeline está esperando a una base de datos lenta; no funcionará mejor. Identifica si el freno es el pensamiento (CPU) o el transporte (I/O) y aplica la medicina correcta.
