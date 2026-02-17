# Alertas y Dashboards: Durmiendo Tranquilo

Monitorizar es ver qué pasa. Alertar es que el sistema te avise cuando algo va mal sin que tú tengas que estar mirando la pantalla.

## 1. Niveles de Alerta
*   **P1 (Crítica):** El sistema está caído o los usuarios no pueden pagar. Debes recibir una llamada o un mensaje de Slack urgente. (Ej: 5% de errores 500 sostenidos).
*   **P2 (Importante):** Hay degradación pero el sistema funciona. Avisar por email o canal de avisos. (Ej: La latencia ha subido a 1 segundo).
*   **P3 (Informativa):** Anomalías detectadas que requieren revisión en horario laboral.

## 2. Dashboards de Operaciones
Crea una pantalla en Grafana que muestre:
1.  **Semáforo:** Verde/Rojo para los Health Checks.
2.  **Top Endpoints Lentos:** ¿Cuáles son las 5 rutas que más hacen sufrir a los usuarios?
3.  **Tasa de Errores por Endpoint:** ¿Es un error global o solo falla `/login`?
4.  **Uso de Recursos:** CPU, RAM y Conexiones a la DB.

## 3. Alertas "Inteligentes" (Anomalía)
En lugar de un límite fijo (ej: > 100 usuarios), usa alertas basadas en el comportamiento histórico. Si normalmente tienes 10 usuarios a las 3 AM y de repente tienes 500, ¡algo pasa!

## 4. On-Call (Guardias)
Establece una rotación de quién es el responsable de atender las alertas P1 fuera del horario de oficina. Sin una rotación clara, las alertas se ignoran y el sistema muere.

## 5. Post-Mortem
Cuando ocurre un incidente grave y se soluciona, escribe un documento:
*   ¿Qué pasó?
*   ¿Por qué pasó? (Los 5 porqués).
*   ¿Cómo evitamos que vuelva a pasar?
*   ¿Nuestras alertas nos avisaron a tiempo?

## Resumen: La API como Ser Vivo
Un backend senior sabe que el software no termina cuando se despliega. El mantenimiento proactivo a través de alertas y dashboards es lo que garantiza la calidad del servicio y la satisfacción (y cordura) del equipo de desarrollo.
