# Patrón Unit of Work (UoW)

El patrón **Unit of Work** se encarga de mantener una lista de objetos afectados por una transacción de negocio y coordina la escritura de estos cambios y la resolución de problemas de concurrencia.

## 1. El problema: Atomicidad Fragmentada

Imagina un servicio que debe:
1.  Actualizar el saldo de un usuario.
2.  Crear una entrada de log.
3.  Enviar una notificación SQL.

Si usas el objeto `session` directamente en 3 repositorios distintos, ¿quién decide cuándo hacer el `.commit()`? Si cada repositorio hace su propio commit, rompes la atomicidad (si el paso 3 falla, el paso 1 ya se guardó).

## 2. La solución: Unit of Work

El UoW actúa como el director de orquesta. Proporciona una interfaz única para confirmar o deshacer todo el conjunto de cambios.

En SQLAlchemy, el objeto `Session` **YA implementa** el patrón Unit of Work. Sin embargo, en arquitecturas limpias, solemos envolverlo para abstraer la dependencia de SQLAlchemy.

## 3. Implementación Conceptual (UoW en Python)

```python
class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.orders = OrderRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
```

## 4. Uso en el Servicio

```python
def process_checkout(user_id, items):
    with UnitOfWork(session_factory) as uow:
        user = uow.users.get(user_id)
        order = uow.orders.create(user, items)
        user.balance -= order.total
        # Al salir del 'with', si no hubo errores, se hace el commit de TODO.
```

## Resumen: Todo o Nada

El Unit of Work garantiza que tu base de datos permanezca consistente. Evita que los repositorios decidan sobre el éxito de la transacción y centraliza esa decisión en la capa de servicios, donde reside la lógica de negocio.
