# CPU-Bound en Python: Saltando el GIL

El GIL (Global Interpreter Lock) es el "villano" en la historia del rendimiento en Python. Su función es proteger la memoria interna de Python para que no haya conflictos, pero a cambio impide que los hilos usen más de una CPU a la vez.

## 1. El síntoma del GIL
Si tienes un código que hace una suma de billones de números y usas `Threading` (hilos):
- Verás que el tiempo de ejecución es igual o PEOR que si lo hicieras en un solo hilo.
- Verás que tu CPU solo usa un núcleo mientras los demás están al 0%.

## 2. La cura: Multiprocessing
Al lanzar procesos separados, cada uno tiene su propia copia de Python. El GIL deja de ser un problema porque cada "instante de Python" corre en un núcleo diferente del procesador sin conocer a los demás.

## 3. Cuándo merece la pena saltar el GIL
- **Procesamiento de Imágenes/Vídeo:** Redimensionar 1.000 fotos.
- **Data Science:** Entrenar modelos pequeños en paralelo o limpiar datasets masivos sin Spark.
- **Criptografía:** Hashear millones de contraseñas.
- **Parsers Pesados:** Procesar miles de archivos XML o JSON gigantes.

## 4. El peligro de la serialización (Pickle)
Para mover datos entre procesos, Python usa `pickle`. 
1. Convierte el objeto a bytes (CPU).
2. Envía los bytes (I/O).
3. Convierte los bytes de vuelta a objeto (CPU).
Si tus datos son muy grandes, el tiempo de "pickling" puede comerse todo el ahorro de tiempo que ganaste con el paralelismo.

## 5. El futuro: Subintérpretes (Python 3.12+)
Las versiones más recientes de Python están introduciendo soporte para múltiples intérpretes dentro del mismo proceso, cada uno con su propio GIL. Esto promete darnos el rendimiento de `multiprocessing` con la ligereza de los `hilos`. Como desarrollador senior, debes seguir esta evolución de cerca.

## Resumen: Elección de Arquitectura
- ¿El código es puro Python matemático? -> **Multiprocessing**.
- ¿El código llama a librerías de C/C++/Rust (como NumPy)? -> **Threading** puede funcionar, ya que esas librerías suelen soltar el GIL por su cuenta.
- ¿El código está esperando a la red? -> **Asyncio/Threading**.
