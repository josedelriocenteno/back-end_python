# Detección de Anomalías: Los ojos que nunca duermen

Tener logs de auditoría es genial, pero si nadie los mira, son inútiles. La detección de anomalías consiste en analizar tus logs en tiempo real buscando patrones que indiquen un ataque en curso.

## 1. Las "Banderas Rojas" (Red Flags)
Configura alertas automáticas cuando ocurra lo siguiente:
- **Pico de 403 Forbidden:** alguien está escaneando IDs que no le pertenecen.
- **Login Brute Force:** 20 fallos de login para el mismo usuario en 1 minuto.
- **Viaje Imposible:** Un mismo usuario se loguea en España y 5 minutos después se loguea en Hong Kong.
- **Data Exfiltration:** Un usuario que normalmente lee 5 registros al día, de repente hace un `SELECT` de 10.000 registros.

## 2. Niveles de Gravedad
- **Info:** Un usuario cambió su email (Normal).
- **Warning:** Alguien falló el login 3 veces (Posible despiste).
- **Critical:** Alguien escaló sus privilegios a Admin sin pasar por el flujo oficial (¡ACCIÓN INMEDIATA!).

## 3. SIEM (Security Information and Event Management)
Para sistemas grandes, no analices los logs con scripts de Python. Usa herramientas profesionales:
- **Splunk:** El estándar corporativo.
- **Datadog Security:** Muy fácil de integrar con APIs modernas.
- **ELK (Elasticsearch/Kibana) con reglas de detección.**

## 4. Respuesta Automática
Si tu sistema detecta una anomalía crítica, puede tomar medidas sin esperar a un humano:
- Bloquear temporalmente la cuenta del usuario.
- Revocar todos los tokens JWT activos para ese ID.
- Activar el modo "Mantenimiento" en el endpoint afectado.

## 5. Falsos Positivos
El mayor enemigo de la detección es el ruido. Si tu sistema envía 100 alertas al día que son "normales", el equipo de desarrollo acabará ignorando la alerta 101 que sí es un ataque real. Ajusta tus límites (Thresholds) constantemente.

## Resumen: Proactividad vs Reactividad
Un desarrollador junior soluciona problemas cuando el cliente llama gritando. Un desarrollador senior soluciona problemas cuando la alerta de anomalía le avisa de un ataque, bloqueándolo antes de que el cliente se dé cuenta.
