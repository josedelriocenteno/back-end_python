# Cómo Evitar y Eliminar Flaky Tests

Un **Flaky Test** es el mayor cáncer de la cultura de ingeniería. Es un test que a veces pasa y a veces falla sin que el código haya cambiado. Genera desconfianza y hace que el equipo ignore fallos reales de producción.

## 1. Fuentes habituales de Flakiness
- **Asincronía mal gestionada:** No esperar a que una tarea de fondo termine.
- **Orden de ejecución:** El Test A deja restos en la DB que hacen fallar al Test B.
- **Dependencia de la Hora:** Tests que fallan solo a medianoche o en años bisiestos.
- **Red/Internet:** Llamadas a APIs externas que a veces tardan más de la cuenta.

## 2. Estrategia: "Aislamiento Radical"
Cada test debe dejar el mundo EXACTAMENTE igual que como lo encontró.
- Usa transacciones de DB con `rollback` automático.
- Usa `fake_fs` para archivos temporales que desaparecen solos.
- Usa `freezegun` para que el tiempo siempre sea el mismo durante el test.

## 3. Cuarentena de Tests
Si detectas un test inestable:
- **NUNCA lo ignores.**
- **Cárcel de Tests:** Muévelo a un archivo especial o márcalo con un decorador `@pytest.mark.flaky`. 
- **Acción:** No permitas que el test vuelva a la suite principal hasta que el desarrollador demuestre que ha pasado 100 veces seguidas sin fallar (`pytest --count=100`).

## 4. Evita los `sleep()`
Si un test tiene `time.sleep(2)`, es un candidato a ser flaky.
- **Solución:** Usa **Polling**. Pregunta "¿Ya está?" en un bucle corto (cada 100ms) hasta un máximo de tiempo. Esto es mucho más robusto y rápido que esperar un tiempo fijo arbitrario.

## 5. Reporteo de Inestabilidad
Usa herramientas que trackeen fallos aleatorios en el CI/CD. Si un test falla 1 vez de cada 50, necesitas saberlo para arreglarlo antes de que se convierta en 1 de cada 5.

## Resumen: Tolerancia Cero
Un desarrollador senior no acepta tests inestables. Es preferible tener 90 tests ultra-fiables que 100 tests de los cuales 5 fallan cuando quieren. La fiabilidad es la moneda de cambio del equipo de QA y Backend.
