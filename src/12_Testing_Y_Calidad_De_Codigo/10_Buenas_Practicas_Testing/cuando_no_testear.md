# ¿Cuándo NO testear? (Saber priorizar)

Aunque parezca una herejía, un desarrollador senior sabe que **no todo debe ser testeado**. El testing tiene un coste de escritura y, sobre todo, un coste de mantenimiento perpetuo. Debes maximizar el ROI (Retorno de Inversión) de tus tests.

## 1. Código Trivial 
No testees getters/setters simples o propiedades que solo devuelven una variable.
- **Ejemplo:** `def get_name(self): return self.name`. 
- Estás testeando el lenguaje Python, no tu App. Es una pérdida de tiempo y ensucia los reportes de cobertura con datos irrelevantes.

## 2. Código Generado Automáticamente
Si usas una herramienta que genera código (como un cliente de API de Swagger), no testees el código generado. Testea **tu uso** de ese código o que el generador funciona, pero no cada línea del output.

## 3. UI que cambia constantemente
En fases muy tempranas de una startup (prototipado), hacer tests E2E de la interfaz puede ser contraproducente. La UI cambiará 5 veces esta semana y tendrás que arreglar los tests 5 veces.
- **Estrategia Senior:** Espera a que la UI sea mínimamente estable antes de automatizarla.

## 4. Código de un solo uso (Scripts desechables)
Un script que vas a ejecutar una vez para migrar 5 filas y que luego vas a borrar probablemente no necesite una suite de tests unitarios completa (a menos que sea una operación de alto riesgo).

## 5. El "Exceso de Seguridad" en Proyectos Pequeños
Si estás haciendo un MVP para validar una idea de negocio, no busques el 100% de cobertura y CI/CD perfecto desde el día 1. 
- **Riesgo:** Gastarás todo el presupuesto en tests y nunca lanzarás el producto.
- **Decisión Senior:** Testea el **Core de Negocio** (el motor de la App) y deja el resto para cuando el negocio sea viable.

## 6. Prototipos y Experimentación
Si estás "jugando" con una nueva librería para ver si sirve, no escribas tests. La fase de experimentación debe ser rápida y sucia. Cuando decidas integrarla de verdad, entonces blinda el código.

## Resumen: Pragmatismo Senior
El testing es una herramienta para ganar confianza y velocidad, no una religión. Aprende a distinguir el código crítico del código efímero. Invierte tus horas de ingeniería donde el riesgo de fallo sea mayor y el impacto en el usuario sea más grave.
