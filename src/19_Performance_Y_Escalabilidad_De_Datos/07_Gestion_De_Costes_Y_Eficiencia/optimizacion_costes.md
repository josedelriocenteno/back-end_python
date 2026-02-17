# Optimización de Costes: Estrategias de FinOps

**FinOps** es la práctica de traer responsabilidad financiera al gasto variable del Cloud. Como ingeniero, tú eres el protagonista de este ahorro.

## 1. El Ciclo de Optimización
1.  **Informar:** Mira tu factura real. ¿Qué servicio gasta más? Usa etiquetas (`labels`) para saber qué equipo está gastando cada euro.
2.  **Optimizar:** Aplica las técnicas que hemos visto (comprimir, particionar, apagar zombies).
3.  **Operar:** Establece alarmas de presupuesto para que el coste no vuelva a subir sin control.

## 2. Rightsizing (Ajuste de Tamaño)
Es muy común elegir una máquina de 16GB de RAM "por si acaso" y luego ver que solo usa 4GB.
*   **Acción:** Reduce el tamaño de tus instancias hasta que la utilización de recursos esté en un punto óptimo (60-80%). Ahórrate el dinero de los recursos desperdiciados.

## 3. Compromiso de Uso (Committed Use Discounts)
Si sabes que vas a usar una base de datos durante los próximos 3 años, Google Cloud te hace un descuento enorme (hasta el 50%) si te comprometes a pagarla por adelantado o mensualmente durante ese tiempo.

## 4. Arquitecturas Event-Driven
En lugar de tener un servidor esperando datos, usa sistemas que solo despierten cuando llega el dato (Pub/Sub + Cloud Functions).
*   **Ahorro:** Pasas de pagar por "estar ahí" a pagar por "hacer algo".

## 5. El coste de la Precisión
A veces, el negocio pide datos en tiempo real pero solo los mira una vez al mes.
*   **Acción:** Propón pasar de Streaming a Batch de 1 hora. La diferencia de coste puede ser de miles de euros y el impacto en el negocio nulo. **Cuestiona los requerimientos caros**.

## Resumen: Eficiencia como Cultura
La optimización de costes no es un evento único, es una disciplina diaria. Un sistema bien diseñado es aquel que es tan barato como sea posible sin comprometer la calidad del servicio. Convierte el ahorro en una métrica de éxito de tu equipo de ingeniería.
