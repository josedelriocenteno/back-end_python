# Cuándo usar (y cuándo NO usar) Machine Learning

El ML es una moda poderosa, pero no es la solución para todo. Usarlo cuando no es necesario añade una complejidad y un coste que pueden hundir un proyecto.

## 1. Cuándo SÍ usar Machine Learning
Úsalo cuando el problema tiene estas características:
*   **Demasiadas reglas:** El problema es tan complejo que escribir reglas `if/else` sería infinito (ej: reconocer caras).
*   **Entornos cambiantes:** Lo que hoy es verdad mañana no lo es (ej: predicción de bolsa o fraude).
*   **Personalización masiva:** Tienes que dar una respuesta diferente a cada uno de tus 10 millones de usuarios (ej: recomendaciones de Netflix).
*   **Patrones ocultos:** Hay relaciones en los datos que un humano no puede ver a simple vista.

## 2. Cuándo NO usar Machine Learning
Huye del ML si:
*   **Reglas claras y fijas:** Si puedes resolverlo con 5 `if/else` que no van a cambiar en años, **usa código tradicional**. Es más rápido, barato y fácil de debugear.
*   **Necesitas explicación total:** El ML a veces es una "caja negra". Si por ley tienes que explicar exactamente por qué se tomó una decisión (ej: denegar un crédito), un modelo complejo puede ser un problema.
*   **No tienes datos:** Sin datos de calidad, el ML no aprende nada (GIGO: Garbage In, Garbage Out).
*   **Coste injustificado:** Si el modelo te ahorra 100€ al mes pero mantener la infraestructura de ML cuesta 1.000€, no tiene sentido.

## 3. La Regla de Oro
> "No uses Machine Learning si una simple consulta SQL o un script de lógica básica resuelve el problema".

## 4. Ejemplos Reales
*   **NO ML:** Calcular el IVA de una factura (Regla fija).
*   **SÍ ML:** Predecir si un cliente va a dejar de pagar su suscripción el mes que viene (Patrón complejo).
*   **NO ML:** Validar que un email tiene una '@' (Formato fijo).
*   **SÍ ML:** Clasificar si un email es una queja, una felicitación o una duda técnica (Lenguaje natural).

## Resumen: Pragmatismo ante todo
El éxito de un ingeniero no es usar la tecnología más compleja, sino la más eficiente para el problema. El Machine Learning es un cañón de precisión; úsalo solo cuando la mosca de tu problema sea demasiado rápida y compleja para ser cazada a mano.
