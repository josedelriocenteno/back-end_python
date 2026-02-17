# Cómo Interpretar Reportes de Test y Cobertura

Un reporte de Pytest lleno de puntos verdes es gratificante, pero ¿qué hacemos cuando las cosas se ponen rojas? Aprender a leer los reportes es una habilidad de debugging esencial.

## 1. El Reporte de Fallo de Pytest
```text
________________ short_test_name ________________
>       assert result == 10
E       AssertionError: assert 8 == 10
```
- **Línea de error:** Te dice exactamente dónde falló.
- **Diferencia (Diff):** Pytest te muestra qué esperaba y qué recibió. En objetos complejos (dicts grandes), usa `-vv` para ver la comparación detallada.

## 2. Los Marcadores de Pytest
- **. (Punto):** El test pasó.
- **F (Fail):** El test falló (falló un assert).
- **E (Error):** Hubo un error de código durante el SETUP o el TEARDOWN (no llegó ni a ejecutarse el assert). ¡Ojo! Esto suele indicar problemas de base de datos o mocks mal configurados.
- **s (Skip):** Test ignorado.
- **x (XFail):** El test falló, pero ya sabíamos que iba a fallar (útil para bugs conocidos que aún no hemos arreglado).

## 3. Interpretando el Mapa de Cobertura
Si miras el reporte HTML de cobertura:
- **Rojo:** Código muerto o no testeado. Preguntas: ¿Es este código necesario? Si es necesario, ¿por qué no hay un test?
- **Parcial (Amarillo):** Suele ocurrir en los `if/else`. Significa que has probado el camino del `if` pero nunca el del `else`. Es un escondite perfecto para bugs de "Error handling".

## 4. Reportes para la Gerencia (JUnit XML)
Si necesitas integrar tus resultados con herramientas como Jira, Jenkins o SonarQube, usa:
```bash
pytest --junitxml=report.xml
```
Esto genera un estándar de la industria que puede ser leído por cualquier software de visualización de calidad.

## 5. El "Wall of Shame" (Tests lentos)
Usa `pytest --durations=10`. 
Te mostrará los 10 tests más lentos de tu suite. Un desarrollador senior revisa esto una vez al mes para optimizar la pipeline. Si un test de integración tarda 15 segundos, hay que ver si está abusando de los comandos `sleep` o si la DB está mal indexada.

## Resumen: Del Dato a la Acción
Un reporte es solo ruido si no tomas decisiones. Úsalo para borrar código muerto, acelerar la pipeline y blindar las zonas rojas de tu mapa de cobertura.
