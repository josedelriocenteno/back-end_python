# Errores Comunes en Testing de Base de Datos

Probar la persistencia es difícil. Estos son los errores que hacen que tus tests sean frágiles, lentos o, peor aún, que den falsos positivos.

## 1. Tests dependientes del orden (Pollution)
*   **Problema:** El Test A inserta un usuario y no lo borra. El Test B asume que la tabla está vacía y falla.
*   **Solución:** Usa transacciones que hagan `ROLLBACK` al final de cada test.

## 2. Mockear el ORM (The Mocking Trap)
*   **Problema:** Usar `unittest.mock` para simular el comportamiento de `session.execute()`.
*   **Por qué es malo:** Estás testeando que tu código llama a una función, no que la query de SQL es correcta. Los Mocks de la DB suelen ser frágiles y ocultan bugs reales de SQL.
*   **Solución:** No mockees la DB. Úsala (aunque sea en memoria).

## 3. No testear las Migraciones
*   **Problema:** Testear contra un esquema creado con `create_all()`.
*   **Impacto:** En producción usas Alembic, pero en tests usas SQLAlchemy. Si falta una migración o hay un error en el script de Alembic, tus tests no lo detectarán.
*   **Solución:** El setup de tus tests de integración debe ejecutar las migraciones de Alembic desde cero.

## 4. Hardcodear IDs en los Asserts
*   **Problema:** `assert user.id == 1`.
*   **Impacto:** Si cambias algo en el setup o añades un registro más, todos tus tests se rompen.
*   **Solución:** Compara por atributos únicos (`username`, `email`) o recupera el ID dinámicamente.

## 5. Ignorar el modo Asíncrono
*   **Problema:** Si tu app usa `asyncio`, tus tests deben usar fixtures asíncronas. Olvidar un `await` en un test puede hacer que pase (falso positivo) sin haber ejecutado nada.

## 6. No limpiar el Identity Map
*   **Problema:** SQLAlchemy guarda objetos en memoria. El test lee el objeto de la RAM del ORM y no de la DB real.
*   **Impacto:** Crees que el campo se guardó bien, pero solo cambió en memoria.
*   **Solución:** Usa `session.expire_all()` o cierra y abre la sesión entre el 'Act' y el 'Assert'.

## Resumen: Tests Robustos = Backend Feliz

Un buen test de base de datos debe ser **aislado**, **repetible** y **fiel a la realidad**. Evita los atajos que ocultan la complejidad de SQL y verás cómo tu confianza al desplegar en producción aumenta drásticamente.
