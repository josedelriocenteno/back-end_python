# CPU-Bound vs I/O-Bound: El diagnóstico inicial

Antes de decidir si usar `asyncio`, `threads` o `processes`, debes identificar qué es lo que está frenando a tu código. Este cuello de botella determinará tu éxito.

## 1. Tareas I/O-Bound (Límite por Entrada/Salida)
Tu código pasa la mayor parte del tiempo **esperando** a que algo externo termine. Tu CPU está prácticamente ociosa (idle) rascándose la barriga.
- **Ejemplos:**
    - Consultar una base de datos.
    - Llamar a una API externa (Stripe, GPT-4, Google Maps).
    - Leer o escribir un archivo en el disco.
    - Esperar a que un usuario envíe un formulario.
- **Solución Senior:** Usar **Concurrencia** (`asyncio`). Mientras esperas la respuesta de la DB, tu código puede estar haciendo otras 100 cosas.

## 2. Tareas CPU-Bound (Límite por Procesador)
Tu código tiene a la CPU echando humo al 100%. Está haciendo cálculos complejos sin parar. No hay esperas externas, solo matemáticas y lógica pura.
- **Ejemplos:**
    - Procesar imágenes (redimensionar, filtros).
    - Cifrado de grandes volúmenes de datos.
    - Minería de datos o cálculos científicos complejos.
    - Compresión de archivos (ZIP, GZIP).
- **Solución Senior:** Usar **Paralelismo** (`multiprocessing`). Divide los cálculos entre los 8 o 16 núcleos de tu procesador.

## 3. El error fatal de diagnóstico
Un error de junior es intentar acelerar una tarea **CPU-Bound** usando `asyncio`. 
- **Resultado:** Tu código no solo no irá más rápido, sino que irá más lento porque añadirás el coste de gestión del `event loop` a una CPU que ya está saturada. El código asíncrono solo es útil cuando hay **pausas** que aprovechar.

## 4. Identificando el cuello de botella (Herramientas)
- **Htop / Task Manager:** Si ves un núcleo al 100% y los demás al 0%, es CPU-Bound pero mal paralelizado.
- **Iostat:** Si el disco está al 100%, es I/O-Bound (Disk).
- **Network Stats:** Si la red está saturada, es I/O-Bound (Network).

## Resumen: Conoce tus límites
- **Muchos clics de espera -> `asyncio`.** (Económico, ligero).
- **Mucho cálculo matemático -> `multiprocessing`.** (Potente, pesado).
- **No estás seguro -> Haz un benchmark.** Mide cuánto tiempo tarda tu código y mira el consumo de CPU durante la ejecución.
