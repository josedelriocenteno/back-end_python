# Límites Reales de Python: ¿Hasta dónde llegar?

Python no es C++ ni Go. Tiene límites físicos y lógicos que debemos conocer para no intentar construir un rascacielos sobre cimientos de barro.

## 1. El Límite de la Memoria
Cada tarea en `asyncio` consume entre 2KB y 5KB de RAM.
- **Cálculo:** 1.000.000 de tareas = ~5GB de RAM solo en "esqueletos" de tareas.
- **Realidad:** Antes de llegar ahí, probablemente mueras por el coste de gestión del Event Loop.

## 2. El Límite del Event Loop
Aunque el Loop sea muy rápido, sigue siendo secuencial. Si tienes 100.000 tareas y cada una tarda 0.1ms en procesarse, el Loop tardará 10 segundos en dar una vuelta completa a todas.
- **Síntoma:** Latencia alta a pesar de CPU baja.

## 3. El Límite del GIL (Vuelve otra vez)
Incluso con `asyncio`, en cuanto Python tiene que hacer algo que no sea esperar (ej: parsear el JSON de respuesta), el GIL entra en juego. Si el JSON es gigante, el GIL bloqueará el Loop.

## 4. Cuándo Python ya no es la herramienta
Como arquitecto senior, debes levantar la mano y decir "Cambiemos de lenguaje" cuando:
- Necesites latencia ultra-baja constante (milisegundos de un solo dígito).
- Tengas que procesar terabytes de datos en tiempo real.
- Tu coste de servidores sea inasumible debido a la ineficiencia de Python ante lenguajes compilados.

## 5. La Regla del 80/20
El 80% de los problemas de backend del mundo se pueden solucionar de sobra con Python asíncrono. Solo el 20% (finanzas de alta frecuencia, motores de juegos, kernels) requieren dar el salto a lenguajes más complejos.

## Resumen: Humildad Técnica
Python es una herramienta increíble para la agilidad y la mayoría de casos de uso de negocio. Conocer sus límites reales te permite diseñar sistemas que los respeten, o saber exactamente cuándo es el momento de delegar una parte crítica del sistema a un microservicio escrito en Rust o Go.
