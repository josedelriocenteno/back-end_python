# Arquitectura Hexagonal y Persistencia

La Arquitectura Hexagonal (o de Puertos y Adaptadores) es el estándar para construir aplicaciones de larga duración que no dependen de sus herramientas externas.

## 1. El Núcleo (Domain)

En el centro del hexágono están tus **Entidades de Dominio** y **Lógica de Negocio**. 
*   **REGLA DE ORO:** El dominio no debe importar nada que huela a base de datos (ni `SQLAlchemy`, ni `psycopg`). 
*   Para el núcleo, el acceso a datos es una "interfaz abstracta".

## 2. Puertos (Interfaces)

Un **Port** es una definición de lo que el núcleo necesita.
```python
# Dominio / Puertos
class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: UserDomainEntity):
        pass
```

## 3. Adaptadores (Implementación)

Un **Adapter** es el código que conecta con el mundo real (PostgreSQL).
```python
# Infraestructura / Adaptadores
class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, db_session):
        self.session = db_session

    def save(self, user: UserDomainEntity):
        # Traducir entidad de dominio a modelo de SQLAlchemy
        model = UserModel.from_domain(user)
        self.session.add(model)
```

## 4. Inversión de Dependencias (DIP)

La Arquitectura Hexagonal da la vuelta a la jerarquía tradicional. 
*   **Arquitectura Tradicional:** El Servicio depende de SQLAlchemy.
*   **Hexagonal:** SQLAlchemy depende de la Interfaz del Servicio.

Esto permite cambiar la base de datos completa simplemente inyectando un Adaptador diferente, sin tocar ni una línea de tu lógica de negocio.

## 5. Cuándo usarla en Backend

1.  **Proyectos Complejos:** Donde esperas estar trabajando más de 2 años.
2.  **Multitenancy:** Si algunos clientes usan Postgres y otros SQL Server.
3.  **Hambre de Testing:** Quieres una suite de tests ultra-rápida que no dependa de Docker/Postgres en cada ejecución.

## Resumen: La Independencia es Libertad

La Arquitectura Hexagonal puede parecer excesiva al principio (más archivos, más clases), pero es la única forma de asegurar que "Postgres es solo un detalle de implementación" y que tu verdadero valor de negocio está protegido de los cambios tecnológicos.
