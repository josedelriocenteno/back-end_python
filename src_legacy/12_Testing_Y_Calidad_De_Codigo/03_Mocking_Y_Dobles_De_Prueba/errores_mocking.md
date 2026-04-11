# Errores Comunes de Mocking (Anti-patrones)

El mocking es como el azúcar: en su justa medida es genial, pero si abusas de él, arruinarás el sistema. Estos son los fallos que convierten una suite de tests en una carga insoportable.

## 1. Mocking de lo que no te pertenece (Third-party)
- **Fallo:** Hacer un mock detallado de la librería `boto3` (AWS) o `requests`.
- **Problema:** Si la librería se actualiza y cambia su comportamiento, tus tests seguirán pasando (porque tu mock es estático), pero tu App fallará en producción.
- **Solución:** Crea un 'Wrapper' (una clase propia) que envuelva la librería. Testea tu Wrapper con la realidad y haz un mock de tu Wrapper en el resto de la App.

## 2. Mocking Excesivo (Doble Acoplamiento)
- **Fallo:** Tienes una función de 10 líneas y haces 8 mocks.
- **Problema:** El test está tan atado a la implementación interna que te impide refactorizar. Si cambias el nombre de una variable privada, el test falla.
- **Regla Oro:** Si puedes evitar el mock usando el objeto real sin que el test sea lento o peligroso, **usa el objeto real**.

## 3. El "Mock de Mock"
- **Fallo:** Hacer un mock que cuando se le llama devuelve otro mock, que a su vez devuelve otro.
- **Resultado:** Código de test ilegible y muy difícil de depurar cuando falla.

## 4. No resetear los Mocks
- **Fallo:** Usar un mock en una fixture con scope amplio (session) y no limpiarlo.
- **Resultado:** El Test B ve que el mock "ya ha sido llamado una vez" (por el Test A) y falla inesperadamente.
- **Solución:** Usa `mock.reset_mock()` o asegúrate de que cada test recibe una instancia fresca.

## 5. Mocks que no devuelven nada (Loose Mocks)
- **Fallo:** Crear un mock y no definir un `return_value`.
- **Resultado:** Por defecto, MagicMock devuelve otro MagicMock. Tu código de negocio seguirá funcionando (sin errores de tipo) pero estará operando con basura. El test pasará pero no estarás probando nada útil.

## 6. Ignorar la Firma del Método (Speccing)
- **Fallo:** Tu función real recibe 2 argumentos, pero tu mock acepta 10 sin quejarse.
- **Solución:** Usa `autospec=True`. Esto obliga al mock a fallar si se le llama con argumentos que no existen en la clase original.

## Resumen: Mockea interfaces, no implementaciones
Un buen mock debe representar un **contrato**. Úsalos solo para aislarte de sistemas externos o componentes muy lentos. Si te encuentras mockeando cada pequeña función auxiliar, es hora de repensar tu arquitectura.
