# Bases de Datos en Memoria (SQLite) para Testing

En el desarrollo Backend, la velocidad de los tests es vital. Una de las formas más comunes de acelerar las pruebas es usar una base de datos en memoria.

## 1. ¿Por qué usar SQLite en memoria?

*   **Velocidad:** No hay I/O de disco ni latencia de red TCP. Es casi instantáneo.
*   **Aislamiento:** Al morir el proceso del test, la base de datos desaparece. No hay que limpiar tablas manualmente.
*   **Paralelismo:** Puedes correr cientos de tests en paralelo, cada uno con su propia DB en memoria sin conflictos.

## 2. Configuración en SQLAlchemy

```python
# La URL especial :memory: indica que es totalmente volátil
engine = create_engine("sqlite:///:memory:")
```

## 3. La trampa de la Compatibilidad

SQLite es excelente, pero **no es PostgreSQL**. Hay muchas cosas que funcionan en uno y no en el otro:
1.  **Tipos de Datos:** SQLite no tiene `JSONB`, `UUID` nativo, ni `INET`.
2.  **Funciones:** Funciones como `DATE_TRUNC` o agregaciones avanzadas de Postgres fallarán en SQLite.
3.  **Constraints:** Algunas constraints de SQLite son más permisivas o se comportan distinto.

## 4. Cuándo NO usar SQLite para Tests

Si tu aplicación hace un uso intensivo de características "Postgres-Only" (lo cual es recomendado en este curso profesional), **debes testear contra Postgres**.

*   **Solución Profesional:** Usa **Testcontainers** (Python) para levantar un contenedor de Docker de Postgres temporal por cada suite de tests.

## 5. Estrategia Híbrida

*   **Tests Unitarios:** Usa SQLite para probar lógica de negocio que no dependa de queries complejas.
*   **Tests de Integración:** Usa una DB real (Postgres) para asegurar que tus Repositorios y Migraciones funcionan perfectamente.

## Resumen: Velocidad vs Fidelidad

No sacrifiques la fidelidad de tus tests por ganar unos segundos si eso significa que los bugs se te escaparán a producción. Usa SQLite para lo simple y Docker/Postgres para lo crítico.
