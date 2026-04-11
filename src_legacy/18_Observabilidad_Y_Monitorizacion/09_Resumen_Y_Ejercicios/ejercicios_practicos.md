# Ejercicios Prácticos: Observabilidad y Calidad

Para consolidar Theme 18, realiza estos ejercicios. No necesitas montar un servidor real, puedes simularlo en scripts de Python o diseñar la arquitectura en papel.

## Ejercicio 1: El Logging Perfecto
Crea un script de Python que simule la carga de un CSV.
*   Debe loguear en nivel `INFO` cuándo empieza y termina.
*   Debe incluir un `correlation_id` aleatorio.
*   Debe loguear un `ERROR` con `exc_info=True` si el archivo no existe.
*   **Bonus:** Usa `jsonlogger` para que el output sea JSON.

## Ejercicio 2: Diseño de Alertas
Imagina un pipeline que lee de Twitter (X) y guarda en BigQuery.
1. Define una **Alerta Crítica** (Síntoma).
2. Define una **Alerta Warning** (Causa).
3. Diseña el contenido del mensaje de Slack que recibiría el equipo.
4. **Solución sugerida:** Crítica: "Llevamos 30 min sin recibir tweets". Warning: "La cuota de la API de X está al 80%".

## Ejercicio 3: Validación con Great Expectations
Describe 3 expectativas que pondrías a una tabla de "Clientes" que contiene: `id`, `email`, `fecha_nacimiento`, `saldo_cuenta`.
*   **Ejemplo:** `expect_column_values_to_match_regex("email", r".+@.+\..+")`.

## Ejercicio 4: Análisis de MTTR
En un incidente, el fallo ocurrió a las 09:00. La alerta sonó a las 09:05. Se arregló a las 09:45.
*   Calcula el tiempo de detección.
*   Calcula el tiempo de resolución.
*   Propón una mejora para bajar el tiempo de detección a 1 minuto.

## Reto Final: El Caso del Modelo Loco
Tu modelo de recomendación de películas de repente empieza a recomendar solo "Titanic" a todo el mundo (niños, adultos, fans del terror).
*   ¿Qué métrica de observabilidad de ML te avisaría de esto antes de que los usuarios se quejen?
*   **Respuesta:** La distribución de las predicciones (Histograma del output del modelo).

## Resumen: Pensamiento Crítico
Estos ejercicios te obligan a dejar de ver el código como algo estático y empezar a verlo como un flujo dinámico que debe ser vigilado, comprendido y protegido constantemente.
