# GitFlow vs. Trunk Based Development

No todos los equipos trabajan igual. Elegir el modelo de branching adecuado define la velocidad de entrega de tu empresa.

## 1. GitFlow: El modelo robusto
Diseñado para lanzamientos programados (ej: una versión cada mes).
- **develop:** Rama donde vive el código de trabajo diario.
- **master/main:** Solo código en producción.
- **release:** Rama para estabilizar una versión antes de lanzarla.
- **Pro:** Control total. Muy difícil que código roto llegue a producción.
- **Contra:** Muy lento y burocrático. Los merges pueden ser una pesadilla.

## 2. Trunk Based Development: El modelo ágil
Diseñado para despliegue continuo (ej: despliegas 10 veces al día).
- Todos trabajan en `main` o en ramas ultra-cortas (horas).
- Se usan **Feature Flags** (interruptores en el código) para que una función nueva llegue al servidor pero no sea visible hasta que esté lista.
- **Pro:** Velocidad máxima. Integración constante.
- **Contra:** Requiere una cultura de testing automatizado impecable. Un fallo en el código rompe el servidor al instante.

## 3. GitHub Flow: El punto medio
El más usado en el mundo Open Source y Startups.
- Ramas de `feature` cortas.
- Pull Requests para revisión.
- Merge directo a `main`.

## 4. Comparativa de Escenarios
- **App de Banco:** Probablemente GitFlow.
- **Red Social / SaaS:** Probablemente Trunk Based o GitHub Flow.
- **Librería Open Source:** Probablemente GitHub Flow.

## Resumen: Evoluciona con tu equipo
Empieza con **GitHub Flow**. A medida que tu equipo crezca y la seguridad sea crítica, muévete hacia GitFlow. Si tus procesos de automatización y tests son increíbles, atrévete con Trunk Based Development.
