# Tipos de Testing: La Pirámide de la Calidad

No todos los tests son iguales. Para tener un sistema robusto sin gastar una fortuna en mantenimiento, debemos entender y equilibrar los diferentes niveles de la **Pirámide de Testing**.

## 1. Unit Testing (Pruebas Unitarias) -> La Base
Prueban la unidad más pequeña de código (una función o una clase) de forma aislada.
- **Velocidad:** Ultra rápidos (milisegundos).
- **Aislamiento:** No tocan base de datos ni internet. Se usan 'Mocks' para las dependencias.
- **Cantidad:** Deberían representar el 70-80% de tus tests.

## 2. Integration Testing (Pruebas de Integración) -> El Centro
Prueban cómo interactúan dos o más componentes reales (ej: tu servicio con la base de datos real).
- **Objetivo:** Detectar fallos en las "fronteras" (ej: una query SQL que falla en Postgres pero funciona en tu cabeza).
- **Velocidad:** Más lentos (segundos).
- **Entorno:** Requieren una DB de test o servicios levantados con Docker.

## 3. E2E Testing (End-to-End / Pruebas de Sistema) -> El Ápice
Prueban el flujo completo desde el punto de vista del usuario (ej: un login real que envía emails y crea registros).
- **Objetivo:** Verificar que todas las piezas encajan.
- **Velocidad:** Muy lentos (minutos).
- **Coste:** Difíciles de mantener porque son frágiles ante cambios menores de UI o red.

## 4. Otros Tipos Especializados
- **Smoke Tests (Pruebas de Humo):** Un conjunto mínimo de tests que se ejecutan tras un deploy para ver si la App "echa humo" (si al menos arranca).
- **Contract Testing:** Aseguran que el frontend y el backend siguen hablando el mismo lenguaje (OpenAPI/Swagger).
- **Load Testing (Pruebas de Carga):** Ver cuántos usuarios aguanta la API antes de colapsar.

## 5. El error de la Pirámide Invertida (El Cono de Helado)
Ocurre cuando una empresa tiene muy pocos unit tests y miles de tests E2E lentos.
- **Resultado:** La pipeline tarda horas en pasar, los desarrolladores ignoran los fallos por "frustración" y el coste de mantenimiento se vuelve insostenible.

## Resumen: Equilibrio Senior
Un buen desarrollador backend sabe situar cada lógica en el nivel adecuado. No hagas un test de integración lento para probar una simple validación de email; para eso están los unit tests. Reserva la artillería pesada para los flujos críticos de negocio.
