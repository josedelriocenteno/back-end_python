# Umbrales, SLAs y SLOs: Midiendo el Compromiso

Para poner alertas, primero debemos definir qué significa "que el sistema vaya bien". Esto se hace mediante métricas de compromiso de nivel de servicio.

## 1. Conceptos Fundamentales
*   **SLA (Service Level Agreement):** El contrato legal con el cliente (ej: "Si la web cae más de 4h al mes, te devuelvo el dinero"). Es un tema de abogados y dinero.
*   **SLO (Service Level Objective):** El objetivo interno del equipo técnico (ej: "Queremos que el 99.9% de las queries tarde < 500ms"). Es más estricto que el SLA para darnos margen de maniobra.
*   **SLI (Service Level Indicator):** La métrica real que medimos (ej: "Latencia actual medida por Prometheus").

## 2. Cómo definir los Umbrales (Thresholds)
No inventes los números. Analiza el histórico de tu sistema:
*   Si tu base de datos suele estar al 30% de CPU, pon la alerta de `Warning` al 70% y la `Critical` al 90%.
*   Si tus procesos Batch suelen tardar 1 hora, alerta si tardan más de 1.5 horas.

## 3. Error Budgets (Presupuesto de Error)
Es un concepto moderno de SRE (Site Reliability Engineering). 
*   Si tu SLO es del 99.9%, tienes un 0.1% de tiempo al mes para fallar. 
*   Si has consumido tu "Error Budget" porque has tenido muchas caídas, **se prohíbe subir código nuevo** hasta que el sistema esté estable otra vez. Solo se permiten arreglos de seguridad.

## 4. Ventanas de Tiempo
Los umbrales deben medirse en ventanas lógicas:
*   **Instantáneos:** Para caídas totales (Down).
*   **Rolling Windows (Ventanas rodantes):** "Media de errores en la última hora". Filtra anomalías estadísticas.

## 5. El papel del Data Engineer
En datos, los umbrales suelen ser sobre la calidad:
*   "SLO: El 95% de las columnas `total_price` no deben ser NULAS".
*   "SLO: El retraso (lag) del pipeline no debe superar los 30 minutos".

## Resumen: Objetivos Claros
Definir SLOs realistas permite al equipo saber cuándo debe dejar de investigar nuevas funciones para centrarse en la estabilidad. Es el lenguaje que une las expectativas del negocio con la realidad técnica de la infraestructura.
