# Métricas de Calidad de Código y Testing

Más allá de la cobertura, existen otras métricas que un desarrollador senior monitoriza para asegurar que el proyecto no se convierta en una "Bola de Lodo" (Big Ball of Mud) inmanejable.

## 1. Complejidad Ciclomática (Cyclomatic Complexity)
Mide cuántos caminos independientes existen a través de tu código.
- **Herramienta:** `Radon` o `Xenon`.
- **Interpretación:** Si una función tiene una complejidad > 10, es demasiado difícil de entender y de testear. Debe ser refactorizada en funciones más pequeñas.

## 2. Índice de Mantenibilidad (Maintainability Index)
Calcula una puntuación de 0 a 100 basada en la complejidad, las líneas de código y el volumen de Halstead.
- **Grado A (100-20):** Código excelente.
- **Grado B (19-10):** Código aceptable.
- **Grado C (< 10):** Código peligroso.

## 3. Duplicación de Código (Copy-Paste detection)
Tener la misma lógica copiada en tres sitios triplica el trabajo de mantenimiento y la probabilidad de bugs.
- **Herramienta:** `flake8-copy-paste-scanner` o herramientas SAST avanzadas.

## 4. Cohesión y Acoplamiento (LCOM)
- **Cohesión:** ¿Las funciones de esta clase realmente están relacionadas?
- **Acoplamiento:** ¿Cuántas clases externas conoce esta clase? Un acoplamiento alto hace que los tests sean muy pesados porque requieren demasiados mocks.

## 5. Tiempo de Ejecución de la Suite (Feedback Loop)
Si tus tests tardan 30 minutos en pasar, los desarrolladores dejarán de ejecutarlos antes de cada commit.
- **Métrica Senior:** Una suite de unit tests debería pasar en menos de 2 minutos. Si tarda más, busca tests lentos o paraleliza.

## Resumen: Datos para Decidir
No refactorices por "instinto". Usa métricas para justificar ante tu equipo o tu manager por qué una parte del código necesita ser reescrita: "Mira, este módulo tiene una Complejidad Ciclomática de 45 y el Índice de Mantenibilidad es de 5. Estamos perdiendo dinero manteniendo esto".
