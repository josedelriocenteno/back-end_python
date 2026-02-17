# Mitos y Errores Conceptuales sobre Rendimiento en Python

La asincronía en Python está rodeada de malentendidos. Desmontar estos mitos es el primer paso para diseñar sistemas backend que no colapsen en producción.

## Mito 1: "Async es multihilo"
**FALSO.** `asyncio` corre en un **UNICO hilo**. Es una forma cooperativa de multitarea. Si una función asíncrona hace un cálculo pesado sin usar `await`, bloqueará a TODA la aplicación. Todos los demás usuarios dejarán de recibir respuesta hasta que esa función termine.

## Mito 2: "Async hace que mi código sea más rápido"
**DEPENDE.** `asyncio` no acelera la ejecución de una sola tarea. Si tu función tarda 2 segundos en calcular algo, en async seguirá tardando 2 segundos. Lo que hace async es permitir que tu servidor maneje **10.000 usuarios lentos** al mismo tiempo, en lugar de bloquearse en el quinto usuario. Mejora el **Throughout** (capacidad), no la **Latencia** (rapidez individual).

## Mito 3: "Threads son mejores que procesos porque pesan menos"
**EN PYTHON, NO SIEMPRE.** Debido al GIL, los hilos en Python compiten por el mismo procesador. Para tareas de cálculo, 4 procesos siempre serán más rápidos que 400 hilos. Los hilos solo son recomendables para tareas I/O muy sencillas o librerías heredadas que no soportan async.

## Mito 4: "Poner 'async' delante de una función ya la hace mágica"
**FALSO.** Si pones `async def mi_funcion()` y dentro haces un `time.sleep(10)`, has acabado con tu servidor. `time.sleep` es síncrono y bloquea el hilo entero. Debes usar siempre las versiones asíncronas de las librerías (`await asyncio.sleep(10)`, `await db.fetch()`, etc.).

## Mito 5: "El paralelismo es la solución a todo"
**FALSO.** Crear un proceso nuevo en el SO es "caro" (consume megabytes de RAM y tarda milisegundos en arrancar). Si tu tarea dura 1 milisegundo, tardarás más en crear el proceso que en hacer la tarea. El paralelismo tiene un "overhead" (coste de gestión) que solo compensa en tareas de larga duración.

## Resumen: Seniority es saber cuándo PARAR
Un desarrollador senior no complica el código añadiendo asincronía o procesos si no hay una necesidad real medida con datos. La simplicidad es la máxima sofisticación; si tu App funciona bien de forma síncrona y no tiene problemas de carga, no le añadas la complejidad del mundo concurrente.
