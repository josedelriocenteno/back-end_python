# Profiling Asíncrono: Detectando Cuellos de Botella

Llegar a la conclusión de que "la App va lenta" es fácil. Saber exactamente **por qué** función asíncrona está bloqueando el Event Loop es el reto del desarrollador senior.

## 1. El Profiling Síncrono no sirve
Herramientas clásicas como `cProfile` a veces tienen problemas para medir correctamente el tiempo de espera (`await`) frente al tiempo de ejecución real en `asyncio`.

## 2. Herramientas Especializadas
- **Pyinstrument:** Es el profiler favorito para Python moderno. Tiene un modo asíncrono excelente que te muestra un "Flame Graph" (Gráfico de llama) indicando dónde se gasta el tiempo.
- **Yappi (Yet Another Python Profiler):** Diseñado específicamente para entender hilos y corrutinas.
- **VizTracer:** Permite ver una línea de tiempo visual de cómo las tareas saltan de una a otra en el Event Loop.

## 3. Detectando el "Event Loop Lag"
Un servidor sano debe tener un tiempo de respuesta del Event Loop casi instantáneo ( < 10ms).
- **Métrica Senior:** Mide cuánto tiempo pasa desde que programas una tarea hasta que empieza a ejecutarse. Si ese tiempo sube, tienes funciones "abusonas" que no están haciendo `await` lo suficiente.

## 4. Debug Mode de Asyncio
Python tiene un modo de depuración nativo muy potente:
```bash
PYTHONASYNCIODEBUG=1 python my_app.py
```
O en código: `asyncio.run(main(), debug=True)`
- **Qué hace:** Te avisará por consola si una tarea tarda más de 100ms en devolver el control al loop. ¡Es la forma más rápida de encontrar bloqueos accidentales!

## 5. Memory Profiling (Filtraciones)
La asincronía puede ocultar fugas de memoria si creas miles de tareas y las dejas en una lista sin limpiar. Usa `tracemalloc` para ver qué objetos están creciendo sin control en tu App async.

## Resumen: No adivines, mide
Un desarrollador senior no hace cambios de rendimiento basados en "intuición". Usa profilers para encontrar el punto exacto donde la CPU se bloquea o el socket espera, y solo entonces aplica la optimización necesaria.
