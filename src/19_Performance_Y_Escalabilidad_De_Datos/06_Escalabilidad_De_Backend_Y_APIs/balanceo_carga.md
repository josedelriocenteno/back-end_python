# Balanceo de Carga: El semáforo del tráfico

Si tienes 10 servidores pero todas las peticiones llegan al mismo, el sistema fallará. El **Balanceador de Carga** (Load Balancer) es el componente que reparte el tráfico de forma inteligente.

## 1. El rol del Load Balancer (LB)
Actúa como un "punto único de entrada". El usuario no llama al servidor directamente, llama al balanceador, y este elige a qué servidor enviar la petición.

## 2. Algoritmos de Reparto
*   **Round Robin:** Envía una petición a cada servidor en orden (1, 2, 3, 1, 2, 3...). Sencillo y efectivo si todos los servidores son iguales.
*   **Least Connections:** Envía la petición al servidor que tenga menos usuarios conectados en ese momento. Ideal para procesos que tardan mucho tiempo.
*   **IP Hash:** Asegura que un mismo usuario (misma IP) siempre llegue al mismo servidor. Útil para sistemas antiguos que guardan datos en memoria local.

## 3. Health Checks (Chequeos de Salud)
El balanceador vigila constantemente a los servidores:
*   "¿Servidor 1, estás ahí?". Si el servidor 1 no responde, el LB lo saca de la lista y el tráfico sigue fluyendo hacia los otros 9.
*   Esto garantiza la **resiliencia** del sistema.

## 4. Tipos de Balanceadores
*   **Capa 4 (L4):** Basado en IP y Puertos. Es ultra-rápido pero no "ve" el contenido de la petición (ej: no sabe qué URL se pide).
*   **Capa 7 (L7):** Basado en HTTP. Puede decidir enviar el tráfico a un servidor u otro según la URL (ej: `/api` va al clúster A y `/images` va al clúster B).

## 5. TLS Termination (Seguridad)
El balanceador suele encargarse de la encriptación HTTPS (SSL/TLS). Libera de este trabajo de CPU a los servidores de aplicaciones, que solo reciben tráfico HTTP plano y rápido.

## Resumen: Puerta de Entrada Segura
Un load balancer es obligatorio en cualquier arquitectura de escalado horizontal. Es el componente que asegura que ningún servidor se sature, que el sistema sea tolerante a fallos y que la experiencia del usuario sea fluida e ininterrumpida.
