# Caché en Backend: Patrones con Redis

Redis es el estándar de la industria para implementar caché en el backend debido a su extrema velocidad y a sus variadas estructuras de datos.

## 1. Patrón: Cache-Aside (Lazy Loading)
Es el más común. La aplicación se encarga de todo.
1. La App busca el dato en Redis.
2. Si está (**Hit**), lo devuelve.
3. Si no está (**Miss**), lo busca en la DB, lo guarda en Redis y lo devuelve.
*   **Pros:** Robusto contra fallos de la caché.
*   **Contras:** El primer usuario siempre tiene un "Miss" (es lento).

## 2. Patrón: Write-Through
Cada vez que la App escribe un dato en la DB, también lo escribe en la caché.
*   **Pros:** La caché siempre está actualizada. No hay "Misses" para datos nuevos.
*   **Contras:** Escribir es un poco más lento porque hay que hacerlo en dos sitios.

## 3. Estructuras de Datos Útiles en Redis
*   **Strings:** Para cachear objetos JSON completos o resultados de queries.
*   **Hashes:** Para guardar perfiles de usuario (objeto campo:valor).
*   **Sorted Sets:** Ideales para "Rankings" o "Top 10" que cambian constantemente.

## 4. Time to Live (TTL) - Tiempo de Vida
Nunca guardes algo en caché para siempre.
*   Define un **TTL** (ej: 60 segundos o 1 hora). Una vez pasado el tiempo, Redis borra el dato automáticamente.
*   Esto garantiza que, tarde o temprano, los datos se refrescarán con la realidad de la base de datos principal.

## 5. Ejemplo conceptual en Python
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_usuario(user_id):
    # Intentamos leer de caché
    cached_user = r.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)
    
    # Si no, vamos a la DB (simulado)
    user = db.query(f"SELECT * FROM users WHERE id={user_id}")
    
    # Guardamos en caché por 1 hora (3600s)
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

## Resumen: El primer escudo
Implementar una caché con Redis es la forma más rápida de duplicar el rendimiento de una API sin cambiar la base de datos ni escalar servidores. Es el primer escudo de defensa ante picos de tráfico y queries pesadas.
