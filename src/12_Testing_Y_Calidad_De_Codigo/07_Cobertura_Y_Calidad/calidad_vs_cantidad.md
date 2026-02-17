# Calidad vs Cantidad: La Mentira del 100% de Cobertura

Es común que las empresas obliguen a sus desarrolladores a llegar al 100% de cobertura de código. Sin embargo, en el mundo real, el **100% de cobertura NO garantiza el 0% de bugs**.

## 1. El Test "Zombie"
Es posible tener cobertura del 100% ejecutando líneas de código sin hacer ningún `assert` real (o haciendo solo asserts de obviedades). Estas líneas cuentan como "testeadas" para la herramienta, pero no están protegidas.

## 2. La Ley de Rendimientos Decrecientes
Pasar del 0% al 80% de cobertura aporta un valor inmenso y previene la mayoría de los bugs.
Pasar del 95% al 100% suele requerir un esfuerzo desproporcionado (tests de excepciones imposibles, tests de getters/setters inútiles) que quita tiempo de desarrollar funcionalidades reales.

## 3. Cobertura de Caminos vs Cobertura de Líneas
```python
def dividir(a, b):
    # Cobertura de línea: llamar con (10, 2) cubre el 100%
    return a / b
```
El test con `(10, 2)` te da un 100% de cobertura, pero si el usuario manda a `b=0`, la App se rompe. El 100% de cobertura te está mintiendo sobre la seguridad de tu función.

## 4. Estrategia Senior: Cobertura Inteligente
No busques el 100% en todo. Prioriza:
- **Core de Negocio (Domain):** 95-100%. Cálculos de precios, lógica de permisos, estados de pedidos.
- **Infraestructura/Glue code:** 60-70%. Controladores, wrappers de APIs externas.
- **UI/Templates:** 20-30%. Es más barato probar esto con tests manuales o de humo.

## 5. Mutación de Tests (Mutation Testing)
Si quieres saber si tus tests son realmente buenos, usa `mutmut` (Mutation Testing en Python).
- La herramienta cambia un `>` por un `<` en tu código fuente y vuelve a ejecutar los tests.
- Si tus tests siguen pasando (en verde), significa que tu test es **malo** porque no ha detectado un cambio crítico en la lógica.

## Resumen: Dormir tranquilo
Un desarrollador senior prefiere un proyecto al 85% con tests de mutación aprobados y lógica de negocio blindada, que un proyecto al 100% lleno de tests frágiles y asserts vacíos.
