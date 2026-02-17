# Lazy vs Eager Loading: El dilema del rendimiento

En un ORM, cuando recuperas un objeto (un Usuario), ¿debería el ORM traer también todos sus objetos relacionados (sus Posts)? La respuesta a esto define si tu aplicación será rápida o sufrirá el temido problema N+1.

## 1. Lazy Loading (Carga Perezosa)
Es el comportamiento por defecto de SQLAlchemy.
*   **Qué hace:** Solo trae los datos de la tabla principal. Si accedes a `user.posts`, en ese momento lanza una SEGUNDA query a la base de datos para traer los posts.
*   **Peligro:** Si iteras sobre 100 usuarios y accedes a sus posts, harás 100 queries extra. Total: 101 queries (Problema N+1).
*   **Error Común:** `DetachedInstanceError`. Si cierras la sesión y luego intentas acceder a `user.posts`, el objeto ya no puede hablar con la DB para traer los datos.

## 2. Eager Loading (Carga Ansiosa)
Le dices a SQLAlchemy que traiga los datos relacionados desde el principio.

### A. Joined Eager Loading (`joinedload`)
Usa un `SQL JOIN` en la misma query.
```python
from sqlalchemy.orm import joinedload
stmt = select(User).options(joinedload(User.posts))
```
*   **Ideal para:** Relaciones One-to-One o Many-to-One.

### B. Selectin Eager Loading (`selectinload`)
Lanza una segunda query usando `IN (id1, id2, ...)` para todos los padres recuperados.
```python
from sqlalchemy.orm import selectinload
stmt = select(User).options(selectinload(User.posts))
```
*   **Ideal para:** Relaciones One-to-Many o Many-to-Many. Es la opción más eficiente para colecciones grandes.

## 3. Cuándo usar cada uno

| Estrategia | SQL Generado | Uso Recomendado |
| :--- | :--- | :--- |
| **Lazy** | Múltiples queries bajo demanda | Relaciones que rara vez se usan en esa vista. |
| **Joined** | 1 Query con JOIN | Relaciones 1:1 o cuando necesitas filtrar por el hijo. |
| **Selectin** | 2 Queries (la 2ª con IN) | Colecciones (1:N, N:N). Evita duplicación de datos en el JOIN. |

## 4. Configuración en el Modelo

Puedes definir el comportamiento por defecto en el `relationship()`, pero lo más profesional es dejarlo como `lazy='select'` (por defecto) y decidir la carga en cada query según la necesidad.

```python
# En el modelo
posts: Mapped[List["Post"]] = relationship(lazy="selectin") # Peligroso, siempre cargará posts
```

## Resumen: Programe con Intención

No dejes que el ORM decida por ti. Usa `selectinload` o `joinedload` explícitamente en tus servicios y repositorios. Si ves en tus logs que una sola petición HTTP genera decenas de queries, tienes un problema de carga perezosa que debes corregir.
