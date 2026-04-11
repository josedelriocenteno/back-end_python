# Stateless vs. Stateful: El diseño para el Cloud

Entender si tu aplicación guarda "recuerdos" o no es lo que determina si podrá escalar a millones de usuarios o si se romperá al primer intento.

## 1. Aplicaciones Stateful (Con Estado)
Son aquellas que dependen de la memoria local del servidor para funcionar.
*   **Ejemplo:** Un chat que guarda los últimos mensajes en una variable global de Python.
*   **Problema:** Si el usuario refresca la página y el Load Balancer lo conecta a otro servidor, el chat estará vacío.
*   **Escalabilidad:** Muy difícil. Requiere "Sticky Sessions" (obligar al usuario a estar en el mismo servidor siempre), lo que impide un balanceo de carga real.

## 2. Aplicaciones Stateless (Sin Estado)
Son aquellas que tratan cada petición como algo totalmente nuevo e independiente.
*   **Funcionamiento:** Toda la información necesaria (quién es el usuario, qué pidió antes) viene en el Token (JWT) o se busca en una base de datos central.
*   **Ejemplo:** Una API REST donde el servidor no recuerda nada entre peticiones.
*   **Escalabilidad:** Perfecta. Puedes tener 1 o 1.000 servidores y el resultado será el mismo; cualquier servidor puede atender a cualquier usuario.

## 3. El reto de los Datos
Para ser Stateless, debes sacar el "Estado" fuera del servidor:
*   **Sesiones:** A Redis.
*   **Archivos subidos:** A Cloud Storage (S3/GCS).
*   **Configuración:** A Variables de Entorno o Secret Manager.

## 4. ¿Cuándo se necesita el Estado?
Incluso en el mundo Cloud, hay sistemas que **deben** ser Stateful por definición:
*   Bases de datos (Postgres, MongoDB).
*   Sistemas de archivos distribuidos.
*   Servicios de mensajería (Kafka, RabbitMQ).
Diseñamos estos sistemas para que sean la "Ancla de Estado" sobre la que se apoyan las APIs Stateless.

## 5. Doce Factores (12-Factor App)
Es una metodología para construir aplicaciones SaaS escalables. Uno de sus puntos clave es precisamente: "Ejecuta la aplicación como uno o más procesos sin estado (stateless)".

## Resumen: Diseña para el Olvido
Si quieres que tu backend sea escalable y profesional, diseña tus funciones y servicios como si sufrieran amnesia entre peticiones. Oblígate a buscar el estado en servicios externos y verás cómo escalar de 1 a 100 servidores se convierte en una tarea trivial y segura.
