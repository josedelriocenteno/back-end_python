# Escalado Vertical: Cuándo y por qué usarlo

Aunque el escalado horizontal es el rey del Cloud, el **Escalado Vertical** (Scale Up) sigue teniendo su lugar y es vital entender sus pros y sus contras.

## 1. ¿En qué consiste?
Consiste en aumentar los recursos de una máquina existente: pasar de 4 núcleos a 16 núcleos de CPU, o de 8GB a 64GB de RAM.

## 2. Ventajas del Escalado Vertical
*   **Simplicidad Extrema:** No necesitas cambiar el código. No necesitas preocuparte por sesiones compartidas o sincronización de red.
*   **Rendimiento en una sola tarea:** Algunas tareas matemáticas pesadas o sistemas monolíticos antiguos no pueden repartirse entre varias máquinas; necesitan una máquina muy potente para terminar rápido.

## 3. Desventajas y Límites
*   **Punto de fallo único:** Si la máquina cae, tu servicio desaparece.
*   **Límite físico:** Eventualmente llegarás a la máquina más potente del mercado y no podrás crecer más.
*   **Coste no lineal:** Un servidor con el doble de potencia suele costar MÁS del doble de dinero.

## 4. ¿Cuándo elegir Escalado Vertical?
1.  **En bases de datos relacionales:** Es más fácil y común dar más RAM y CPU a un PostgreSQL que particionarlo en varios servidores (Sharding).
2.  **En etapas iniciales (MVP):** Es más rápido lanzar una máquina un poco más grande que configurar un clúster de Kubernetes con auto-scaling.
3.  **Procesamiento Batch:** Si tienes un script de Python que procesa un archivo muy grande una vez al día, es más barato y simple darle 128GB de RAM a esa tarea específica que intentar repartirla.

## 5. El camino hacia el Cloud
Hoy en día, el escalado vertical es "virtual". Puedes cambiar el tipo de instancia en GCP o AWS con un solo clic y un reinicio de 1 minuto. Esto permite empezar en vertical y, cuando la App madure y la carga crezca, migrar a una arquitectura de escalado horizontal.

## Resumen: Simplicidad antes de Complejidad
El escalado vertical es tu primer paso para ganar velocidad. No lo desprecies por ser "clásico"; úsalo cuando la simplicidad sea más valiosa que la elasticidad infinita, especialmente en sistemas de bases de datos y tareas de procesamiento único.
