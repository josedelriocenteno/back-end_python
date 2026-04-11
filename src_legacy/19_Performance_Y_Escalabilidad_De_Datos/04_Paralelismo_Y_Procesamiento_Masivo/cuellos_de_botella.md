# Cuellos de Botella en el Procesamiento Masivo

Aumentar el paralelismo no siempre acelera el proceso. Existe un punto donde añadir más recursos empeora las cosas. Estos son los cuellos de botella más comunes.

## 1. La Ley de Amdahl
La velocidad máxima de un sistema está limitada por su parte **secuencial**.
*   Si el 10% de tu código no se puede paralelizar (ej: guardar el resultado final en un solo archivo), da igual que tengas 1.000 núcleos; nunca irás más de 10 veces más rápido que con un solo núcleo.

## 2. Data Skew (Sesgo de Datos) - El problema del "Worker Lento"
Ocurre cuando el trabajo no se reparte bien.
*   **Ejemplo:** Particionas por `cliente`. El cliente "Amazon" tiene 1 millón de filas y el cliente "Panadería Pepe" tiene 10.
*   **Impacto:** Un servidor termina en 1 segundo y el otro tarda 1 hora. Tu pipeline total tarda 1 hora porque tiene que esperar al más lento.
*   **Solución:** Busca una clave de partición más uniforme (un hash) o usa técnicas de "rebalaceo".

## 3. Network Overhead (Sobrecarga de Red)
En sistemas distribuidos, mover datos de un servidor a otro ("Shuffling") es lentísimo.
*   Si tus procesos paralelos pasan más tiempo enviándose datos entre ellos que procesándolos, el paralelismo es inútil.
*   **Estrategia:** Intenta que el proceso ocurra lo más cerca posible de donde están los datos físicamente.

## 4. Resource Contention (Pelea por Recursos)
Incluso con muchos núcleos de CPU, todos los procesos suelen pelearse por un único recurso compartido: **El Disco** o **El Ancho de Banda de Red**.
*   Si 100 hilos intentan escribir en el mismo archivo a la vez, el disco se bloquea y todo el sistema se frena.

## 5. El coste de la coordinación
Gestionar la sincronización entre miles de tareas paralelas consume CPU y memoria. Existe un número óptimo de trabajadores para cada tarea; pasarse de ese número es tirar el dinero y el rendimiento.

## Resumen: El equilibrio del paralelo
Paralelizar es un arte de equilibrio. Debes evitar el sesgo en el reparto de datos, minimizar el movimiento de información por la red y entender que hay partes de tu código que siempre serán lentas. Identificar estos cuellos de botella es lo que permite optimizar procesos de Big Data reales.
