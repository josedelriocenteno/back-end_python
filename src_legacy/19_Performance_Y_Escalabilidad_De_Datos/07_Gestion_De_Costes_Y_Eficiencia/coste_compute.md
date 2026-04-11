# El Coste del Cómputo: Pagar solo por lo que usas

En la nube, el cómputo (CPU y RAM) es a menudo el gasto más grande. El performance no es solo velocidad, es la capacidad de hacer la misma tarea con menos recursos.

## 1. El modelo de pago por tiempo
La mayoría de los servicios de nube cobran por el tiempo que la máquina está encendida y sus especificaciones.
*   **Gasto Inútil:** Un servidor encendido al 5% de uso las 24 horas del día.
*   **Eficiencia:** Un servidor que se enciende cuando hay trabajo (Serverless) y se apaga al terminar.

## 2. Serverless y el coste por ejecución (Cloud Run / Functions)
En este modelo, el performance es dinero directo.
*   Si tu función tarda 2 segundos en responder debido a un código ineficiente, pagas el doble que si tardara 1 segundo.
*   **Optimización:** Minimiza el tiempo de arranque ("Cold Start") y optimiza la lógica principal para que sea lo más rápida posible.

## 3. Spot Instances (Instancias de Excedente)
Permiten usar máquinas con un descuento de hasta el 90%.
*   **El truco:** Google/AWS pueden apagarte la máquina en cualquier momento si necesitan el recurso para un cliente que paga el precio completo.
*   **Uso:** Procesamiento de datos en batch que sea **Idempotente** y soporte reintentos. Es la mejor forma de ahorrar en tareas pesadas de Big Data.

## 4. Eficiencia en el Lenguaje
A gran escala, el lenguaje importa.
*   Un script de Python puede necesitar 4 núcleos para procesar 1 millón de registros en 1 minuto.
*   El mismo programa en Go o Rust podría necesitar solo 1 núcleo y medio minuto.
*   Ahorras un 75% en la factura de cómputo solo por cambiar de tecnología en procesos ultra-repetitivos.

## 5. El peligro de los "Zombies"
Es muy común dejar máquinas de desarrollo o de pruebas encendidas durante los fines de semana. 
*   **Solución:** Automatiza el apagado de recursos fuera de horas laborables.

## Resumen: Ingeniería Financiera
Optimizar el cómputo es una de las tareas más agradecidas de un Data Engineer. Lograr procesos rápidos que ocupen poca memoria permite usar instancias más pequeñas y apagar los recursos antes, impactando directamente en la rentabilidad del proyecto.
