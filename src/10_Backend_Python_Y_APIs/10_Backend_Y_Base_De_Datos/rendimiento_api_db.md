# Rendimiento: Optimizando la unión API + Base de Datos

El 90% de los cuellos de botella de una API lenta no están en el código de Python, sino en cómo el código se comunica con la base de datos.

## 1. El pecado original: N+1
*   **Problema:** Pides una lista de 50 usuarios y, por cada uno, haces una query extra para traer sus posts. **Resultado: 51 queries.**
*   **Solución:** Usa `joinedload` (para 1-a-1) o `selectinload` (para 1-a-muchos).
    `db.query(User).options(joinedload(User.profile)).all()` -> **Resultado: 1 sola query.**

## 2. Peticiones innecesarias (Lazy Loading)
Por defecto, SQLAlchemy no trae las relaciones (Lazy). Esto es bueno para ahorrar memoria, pero si en tu Schema de Pydantic pides ese campo, SQLAlchemy lanzará la query automáticamente en el último momento, causando lentitud.
*   **Tip Senior:** Configura tus relaciones como `lazy='raise'` durante el desarrollo. Así, si olvidas un eager load, la app explotará y podrás arreglarlo antes de que llegue a producción.

## 3. Connection Pooling (Pool de Conexiones)
Abrir una conexión a Postgres tarda tiempo (handshake TCP, Auth).
*   **Solución:** Mantén un pool de 10-20 conexiones abiertas y reutilízalas. SQLAlchemy lo hace por defecto, pero debes configurar el `pool_size` y `max_overflow` según la capacidad de tu servidor.

## 4. Índices y "Select *"
*   **Índices:** Si filtras por `email` frecuentemente, añade un índice en esa columna.
*   **Atributos específicos:** Si solo necesitas el `id` y el `name`, no pidas toda la fila.
    `db.query(User.id, User.name).all()` es mucho más rápido y ligero que `db.query(User).all()`.

## 5. El impacto de los Bloqueos (Locking)
Las transacciones largas (mucho código entre el inicio y el commit) bloquean filas de la base de datos. Otros usuarios intentando leer o escribir esas filas tendrán que esperar (latencia alta).
*   **Solución:** Mantén tus transacciones lo más cortas posible. Ejecuta la lógica pesada de cálculo ANTES de abrir la transacción o el commit.

## 6. Base de Datos de Solo Lectura (Read Replicas)
En APIs con muchísimo tráfico, usamos dos conexiones:
*   `GET` -> Van a una réplica de lectura de Postgres (barato y rápido).
*   `POST/PUT/DELETE` -> Van al nodo maestro (caro y consistente).

## Resumen: Mide y vencerás
Usa herramientas como **SQLAlchemy Query Counter** en tus tests para asegurar que no estás lanzando más queries de las que crees. Una API optimizada es una API que trata a su base de datos con respeto y eficiencia.
