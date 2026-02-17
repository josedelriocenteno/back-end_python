# Bases de Datos en Memoria y Testcontainers

Aislar el estado de la base de datos es el mayor reto en el testing de backend. Estas son las dos estrategias profesionales para gestionar bases de datos de prueba.

## 1. SQLite en Memoria (`sqlite:///:memory:`)
Es la opción por defecto para la mayoría de proyectos pequeños y medianos.
- **Pros:** Extremadamente rápida (milisegundos). No requiere instalar nada fuera de Python. Se borra sola al terminar el test.
- **Contras:** SQLite no soporta todas las funciones de PostgreSQL o MySQL (ej: tipos `JSONB`, `ARRAY`, o búsquedas de texto avanzadas).
- **Ideal para:** Unit testing y lógica de negocio sencilla.

## 2. Testcontainers (El estándar Senior)
Permite levantar una base de datos **idéntica a la de producción** dentro de un contenedor Docker temporal durante la ejecución de Pytest.
```python
from testcontainers.postgres import PostgresContainer

with PostgresContainer("postgres:15") as postgres:
    engine = create_engine(postgres.get_connection_url())
    # Tu DB de producción real, corriendo en segundos
```
- **Pros:** Pruebas 100% realistas. Soporta todas las funciones específicas de tu DB corporativa.
- **Contras:** Requiere tener Docker instalado. Más lento que SQLite (tarda ~2-5 segundos en arrancar).
- **Ideal para:** Integration testing y pruebas de rendimiento.

## 3. Estrategia de Purga (Cleanup)
Independientemente del motor, el estado debe ser puro para cada test.
- **TRUNCATE:** Borrar datos de las tablas sin borrar el esquema. Mucho más rápido que recrear la DB entera.
- **Transaction Rollback:** Inicias una transacción al inicio del test y haces `rollback` al final. Los datos nunca llegan a confirmarse en el disco. Es la técnica más rápida para tests concurrentes.

## 4. Datos de Semilla (Seeding)
Evita tener archivotes SQL de 10.000 líneas para poblar la DB de test.
- Usa **Fixtures de Pytest** que inserten solo lo necesario para ese test.
- Usa **Model Factories** (como `factory_boy`) para generar objetos de DB complejos con relaciones de forma declarativa.

## Resumen: Fiabilidad vs Velocidad
Como desarrollador senior, usarás SQLite para el 90% de tus unit tests de lógica, y Testcontainers para ese 10% de integración crítica donde PostgreSQL se comporta de forma diferente. Nunca permitas que los tests de DB se ejecuten contra el servidor de desarrollo compartido.
