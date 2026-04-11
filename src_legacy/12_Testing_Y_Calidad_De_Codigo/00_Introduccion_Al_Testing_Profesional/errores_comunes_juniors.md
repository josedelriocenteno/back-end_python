# Errores Comunes de Testing (Nivel Junior)

Escribir tests no es suficiente; hay que escribir tests **útiles**. Muchos equipos pierden el tiempo manteniendo código de test que no aporta valor real o que, incluso, oculta bugs.

## 1. Testear Implementación, no Comportamiento
- **Fallo:** Hacer un test que comprueba "si la función llamó a la línea 42 con el parámetro X".
- **Realidad:** Si cambias una línea de código interna sin cambiar el resultado, el test falla. Esto hace que el refactor sea un infierno.
- **Solución:** Testea qué entra y qué sale. Si el resultado es correcto, no importa cómo se calculó por dentro.

## 2. Cobertura Vacía (Testing for Coverage)
- **Fallo:** Hacer tests que ejecutan el código pero no comprueban nada (`assert True`). Solo para subir el porcentaje de cobertura un 100%.
- **Consecuencia:** Tienes un 100% de cobertura pero la App está rota. Es una falsa sensación de seguridad peligrosa.

## 3. Tests que dependen de la Red o la DB Real
- **Fallo:** Un unit test que falla si el ordenador no tiene internet porque intenta llamar a la API de Google.
- **Fallo:** Un test que falla porque el compañero borró un registro de la base de datos de "pruebas" compartida.
- **Solución:** Los unit tests deben ser deterministas y aislados. Usa Mocks o bases de datos efímeras que se resetean siempre.

## 4. Lógica Compleja dentro de los Tests
- **Fallo:** Escribir tests con `if`, `for` y lógica enrevesada.
- **Realidad:** ¿Quién testea a los tests? Un test con lógica compleja probablemente tenga sus propios bugs.
- **Solución:** El código de test debe ser plano, aburrido y extremadamente fácil de leer.

## 5. Omitir los Casos de Borde (Edge Cases)
- **Fallo:** Probar solo el "camino feliz" (Happy Path) donde el usuario introduce todo bien.
- **Realidad:** El 90% de los bugs ocurren en los extremos: entradas vacías, números negativos, fechas futuras, strings gigantes.

## 6. Tests Frágiles (Flaky Tests)
- **Fallo:** Tests que a veces pasan y a veces fallan sin cambiar el código (normalmente por problemas de asincronía o red).
- **Consecuencia:** Los desarrolladores dejan de confiar en la pipeline. "Bah, ha fallado el test de pago, dale a reintentar que suele pasar".
- **Solución:** Un test inestable debe ser arreglado o borrado inmediatamente antes de que envenene la cultura de calidad del equipo.

## Resumen: Calidad sobre Cantidad
Diez tests bien diseñados que prueban casos críticos valen más que cien tests automáticos que solo prueban getters y setters. Aprende a identificar qué es lo que realmente puede romperse y enfoca tu energía allí.
