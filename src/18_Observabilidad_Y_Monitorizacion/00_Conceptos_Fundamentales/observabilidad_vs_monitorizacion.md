# Observabilidad vs. Monitorización

Aunque mucha gente usa estos términos como sinónimos, representan niveles diferentes de madurez en la gestión de sistemas.

## 1. Monitorización: "¿Está el sistema vivo?"
La monitorización es reactiva. Se basa en reglas predefinidas y respuestas binarias.
*   **Pregunta:** "¿Se ha caído el servidor?".
*   **Respuesta:** "Sí, manda un email".
*   **Limitación:** Si ocurre algo nuevo que no habías previsto (un "Desconocido de lo Desconocido"), la monitorización no te dirá nada.

## 2. Observabilidad: "¿Por qué ha pasado esto?"
La observabilidad es proactiva y exploratoria. Se centra en el estado interno a través de los datos.
*   **Pregunta:** "¿Por qué el 5% de las compras de usuarios de iPhone en España están fallando desde las 10:00?".
*   **Respuesta:** Los logs y las trazas te permiten cruzar datos y descubrir que hay un error en el parsing de un campo específico que solo envía la app de iOS v2.1.

## Tabla Comparativa

| Característica | Monitorización | Observabilidad |
| :--- | :--- | :--- |
| **Enfoque** | Externo (Health checks) | Interno (Contexto rico) |
| **Estado** | Binario (Up/Down) | Continuo (Salud y causas) |
| **Acción** | Alerta ante fallos conocidos | Diagnóstico ante fallos nuevos |
| **Herramienta** | Dashboard con luces rojas | Herramientas de análisis de logs/trazas |

## Aplicado a Datos
*   **Monitorización:** Avisa si el proceso de Airflow falla.
*   **Observabilidad:** Te permite ver que el proceso de Airflow "funcionó", pero que la tabla de destino tiene 0 filas porque la API de origen devolvía un JSON vacío.

## Resumen: La evolución
La monitorización te dice QUE hay un problema. La observabilidad te dice DONDE y POR QUE. Necesitas ambas para construir una plataforma de datos industrial y resiliente.
