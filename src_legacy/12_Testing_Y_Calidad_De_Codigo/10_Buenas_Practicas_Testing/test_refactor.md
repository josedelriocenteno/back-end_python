# Refactorización de Tests: Manteniendo la Suite Viva

Los tests son código, y como todo código, acumulan deuda técnica. Si no refactorizas tus tests periódicamente, se volverán lentos, difíciles de leer y acabarán siendo una carga que el equipo querrá borrar.

## 1. El test también se "Limpia" (DRY en Tests)
Si ves que 10 tests diferentes están creando el mismo objeto de usuario complejo a mano:
- **Refactor:** Crea una **Fixture** o una **Factory**.
- **Beneficio:** Si mañana el modelo de usuario cambia (ej: añades un campo obligatorio), solo tienes que actualizar la factory en un sitio, no en 10 tests.

## 2. Eliminar "Magic Numbers" en los Asserts
- **Mal:** `assert result == 121.0`
- **Bien:** `assert result == base_price + (base_price * TAX_RATE)`
- **Por qué:** Si el IVA cambia del 21% al 22%, el segundo test se entiende y se arregla solo. El primero parece un número aleatorio "mágico".

## 3. De-acoplamiento de la Implementación
Si tu test falla cada vez que cambias un detalle interno del código (como el nombre de una variable privada), tu test está **demasiado acoplado**.
- **Refactor:** Asegúrate de que tus tests prueban la **API pública** de tus módulos, no los detalles de implementación internos.

## 4. Tests Obsoletos
A veces una funcionalid cambia tanto que el test original ya no tiene sentido.
- **Acción Senior:** No tengas miedo de borrar o reescribir un test. Un test que protege un comportamiento que ya no existe es solo ruido.

## 5. El archivo `conftest.py` como librería
Mueve las fixtures genéricas a `conftest.py` para limpiar los archivos de test y dejar solo la lógica de comprobación.

## Resumen: El jardinero de la calidad
Un desarrollador senior dedica un porcentaje de su tiempo a "podar" la suite de tests. Elimina duplicidades, acelera las fixtures lentas y mejora los nombres. Una suite de tests limpia es un placer de usar; una suite sucia es una pesadilla de mantenimiento.
