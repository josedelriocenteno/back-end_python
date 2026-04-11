# Evitando Deadlocks y Livelocks

En el desarrollo concurrente avanzado, los bloqueos entre hilos o procesos son la pesadilla recurrente. Un **Deadlock** es un estado donde dos o más tareas se esperan mutuamente para siempre.

## 1. La Regla del Orden de los Locks
Si tu código necesita obtener dos locks (A y B) para realizar una tarea:
- **MAL:** El Hilo 1 pide A -> B. El Hilo 2 pide B -> A. (Posible Deadlock).
- **BIEN:** Define un orden jerárquico. Todo el código del proyecto DEBE pedir siempre los locks en el mismo orden (primero A, luego B).

## 2. Timeout en los Locks
Nunca uses un Lock que no tenga tiempo límite (si la librería lo permite).
- **Estrategia Senior:** En lugar de `lock.acquire()`, usa `lock.acquire(timeout=5)`. Si no consigues el lock en 5 segundos, retrocede, libera lo que tengas y vuelve a intentarlo más tarde o lanza un error controlado.

## 3. Livelock: Correr sin avanzar
Ocurre cuando dos tareas están tan ocupadas respondiendo a las acciones de la otra que ninguna avanza. Es como dos personas que se encuentran en un pasillo y ambas intentan esquivarse hacia el mismo lado simultáneamente una y otra vez.
- **Solución:** Añade un reintento con tiempo aleatorio (Jitter) para romper la sincronía perfecta que causa el Livelock.

## 4. Starvation (Hambre de Recursos)
Ocurre cuando una tarea de alta prioridad acapara todos los recursos y las tareas de baja prioridad nunca llegan a ejecutarse.
- **Solución:** Implementa sistemas de "Fair Quotas" (cuotas justas) o envejecimiento de tareas (cuanta más vieja sea una tarea, más prioridad gana).

## 5. El peligro de 'await' dentro de un Lock
Hacer un `await` (que puede durar segundos) mientras mantienes un Lock es una receta para el desastre. Bloquearás a todos los demás hilos durante todo ese tiempo.
- **Regla de Oro:** Los Locks deben mantenerse durante el menor tiempo posible, idealmente solo para operaciones de memoria rápidas.

## Resumen: Fluidez ante todo
Un sistema concurrente bien diseñado es como una autopista con tráfico fluido. Los Locks son los semáforos; si pones demasiados o están mal sincronizados, causarás un atasco gigante. Usa locks solo cuando sea estrictamente necesario y siempre con una estrategia de salida.
