# Aprendizaje por Refuerzo: Aprender por ensayo y error

Es el tipo de aprendizaje más parecido a cómo aprenden los seres vivos o cómo se entrena a una mascota. Se basa en un sistema de **Premios y Castigos**.

## 1. Los Componentes
*   **Agente:** El "cerebro" que está aprendiendo (un robot, un software).
*   **Entorno:** El mundo donde vive el agente (un nivel de un juego, la bolsa de valores).
*   **Acción:** Lo que el agente decide hacer (ir a la izquierda, comprar una acción).
*   **Recompensa (Reward):** Un número que dice si la acción fue buena (+10) o mala (-5).

## 2. ¿Cómo funciona?
El agente no sabe nada al principio. Empieza a moverse al azar.
1. Realiza una acción.
2. Recibe una recompensa (o castigo).
3. Actualiza su estrategia para maximizar la recompensa total a largo plazo.

## 3. Casos de Uso Famosos
*   **Videojuegos:** Agentes que aprenden a jugar al Ajedrez, Go o videojuegos (AlphaGo).
*   **Robótica:** Robots que aprenden a caminar o a mover objetos sin ser programados paso a paso.
*   **Coches Autónomos:** Aprender a mantenerse en el carril y evitar obstáculos.
*   **Trading:** Algoritmos que aprenden cuándo comprar o vender para ganar dinero.

## 4. Exploración vs. Explotación
Es el gran dilema del aprendizaje por refuerzo:
*   **Exploración:** Probar cosas nuevas para ver si hay una recompensa mejor.
*   **Explotación:** Seguir haciendo lo que ya sabe que da recompensa.
Un buen agente debe equilibrar ambas para no quedarse estancado en una estrategia mediocre.

## 5. Complejidad Técnica
Es el tipo de ML más difícil de implementar y de entrenar. Requiere muchísima potencia de cómputo y millones de simulaciones para que el agente aprenda algo útil.

## Resumen: Aprender jugando
El aprendizaje por refuerzo es el futuro de la autonomía. Permite crear sistemas que no solo predicen el futuro, sino que interactúan con él y mejoran sus decisiones a base de experiencia directa en mundos complejos y dinámicos.
