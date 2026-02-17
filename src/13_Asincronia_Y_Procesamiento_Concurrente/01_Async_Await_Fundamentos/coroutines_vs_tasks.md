# Corrutinas vs Tareas (Tasks)

Aunque a menudo usamos los términos indistintamente, en `asyncio` existe una diferencia técnica crucial entre una **Corrutina** y una **Tarea**. Saber cuándo usar cada una optimiza el rendimiento de tu API.

## 1. La Corrutina (El Objeto)
Es lo que devuelve una función `async def`. Es simplemente una receta para algo que se puede ejecutar, pero que está "dormido".
- **Estado:** Pasivo.
- **Ejecución:** Solo se ejecuta cuando alguien hace un `await` sobre ella.
- **Flujo:** Es secuencial. El código se detiene en el `await` hasta que la corrutina termina.

## 2. La Tarea (El Proceso de Ejecución)
Es un envoltorio (wrapper) alrededor de una corrutina que el Event Loop programa para que se ejecute **lo antes posible**.
- **Estado:** Activo / Programado.
- **Creación:** `asyncio.create_task(mi_corrutina())`.
- **Flujo:** No bloqueante. El código continúa a la siguiente línea mientras la tarea se ejecuta "en paralelo" (concurre) en el fondo.

## 3. Comparativa Visual
```python
# SECUENCIAL (Lento): Tarda 2 segundos
await tarea_1() # Espera 1s
await tarea_2() # Espera 1s

# CONCURRENTE (Rápido): Tarda 1 segundo
t1 = asyncio.create_task(tarea_1())
t2 = asyncio.create_task(tarea_2())
# Ambas están ya corriendo...
await t1
await t2
```

## 4. ¿Cuándo usar cada una?
- **Usa Corrutinas (`await` directo):** Cuando una tarea depende estrictamente del resultado de la anterior. (Ej: obtener ID -> luego obtener datos de ese ID).
- **Usa Tareas (`create_task`):** Cuando tienes varias cosas que no dependen entre sí. (Ej: enviar 5 emails, consultar 3 APIs distintas).

## 5. El peligro de 'Fire and Forget' (Disparar y olvidar)
A veces creas una tarea y no haces `await` sobre ella.
- **Riesgo:** Si el Event Loop se cierra antes de que la tarea termine, la tarea morirá a medias de forma silenciosa. Además, las excepciones dentro de la tarea no se verán hasta que alguien las recoja.

## Resumen: Programación vs Ejecución
Piensa en la **corrutina** como un archivo de música (.mp3) y en la **tarea** como el reproductor que lo está haciendo sonar. Puedes tener mil archivos en el disco, pero solo consumen memoria real cuando los pones a sonar en el Event Loop.
