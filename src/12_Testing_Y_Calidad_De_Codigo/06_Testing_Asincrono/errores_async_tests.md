# Errores en Tests Asíncronos (Flaky Tests)

Los tests asíncronos son los culpables del 90% de los "Flaky Tests" (tests que fallan aleatoriamente) en las pipelines profesionales. Estos fallos "fantasma" destruyen la confianza del equipo.

## 1. El Await Olvidado
Es el error número uno.
```python
async def test_vulnerable():
    # Lanzamos el proceso pero NO lo esperamos
    db.save_user(user) 
    # Comprobamos el resultado... ¡pero la DB aún no ha guardado!
    assert db.count_users() == 1
```
- **Consecuencia:** A veces el procesador es rápido y pasa; a veces es lento y falla.
- **Solución:** Activa los warnings de `unawaited coroutine` en Python.

## 2. Race Conditions (Condiciones de Carrera)
Ocurre cuando dos tareas asíncronas intentan modificar el mismo recurso de test al mismo tiempo.
- **Ejemplo:** Dos tests asíncronos borrando la misma tabla de base de datos simultáneamente.
- **Solución:** Cada test asíncrono debe tener su propio prefijo de datos o su propio esquema de base de datos aislado.

## 3. Timeouts demasiado estrictos
Un test que pasa en 100ms en tu Macbook de 3000€ puede tardar 2 segundos en un servidor de CI/CD barato y cargado de trabajo.
- **Solución:** Sé generoso con los tiempos de espera en los tests. Un test que espera 5 segundos no es malo si garantiza estabilidad.

## 4. Bucle de Eventos compartido
Si un test asíncrono deja el bucle de eventos en un estado "sucio" (tareas pendientes sin cerrar), el siguiente test puede heredar problemas extraños.
- **Solución:** Asegúrate de que cada test crea su propio bucle de eventos (`scope="function"`) o usa la gestión automática de Pytest-asyncio.

## 5. Mocks Asíncronos mal configurados
Si intentas hacer un `await` a un `MagicMock` normal, fallará porque el Mock no es una corrutina.
- **Solución:** Usa `AsyncMock` de `unittest.mock`. Está diseñado para ser "awaitable" y devolver corrutinas.

## Resumen: Estabilidad ante todo
Un test asíncrono es una pieza de ingeniería delicada. Si no estás seguro de poder hacerlo determinista, es mejor hacerlo síncrono sacrificando un poco de velocidad. La estabilidad de la pipeline es mucho más valiosa que ganar unos milisegundos.
