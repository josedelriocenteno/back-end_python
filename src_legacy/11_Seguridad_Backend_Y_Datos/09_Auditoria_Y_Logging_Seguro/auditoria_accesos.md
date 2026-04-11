# Auditoría de Accesos: El Rastro de Boronas

La auditoría no es logging normal. Mientras el logging sirve para saber por qué se rompió algo, la auditoría sirve para saber **QUIÉN hizo QUÉ y CUÁNDO**. Es una herramienta legal y de seguridad.

## 1. Eventos Críticos para Auditar
No loguees cada `GET`. Registra solo las acciones mutables o sensibles:
- Logins (Éxitos y Fallos).
- Cambios de contraseña.
- Creación/Borrado de usuarios.
- Exportación masiva de datos (ej: descargar CSV de clientes).
- Cambios en roles o permisos.

## 2. La Anatomía de un Registro de Auditoría
Cada entrada debe contener:
- **Timestamp:** Cuándo ocurrió (en UTC).
- **Actor:** ID del usuario que realizó la acción.
- **Acción:** `CREATE`, `UPDATE`, `DELETE`, `LOGIN`.
- **Recurso:** Sobre qué objeto (ej: `Invoices`, `id: 502`).
- **IP / UserAgent:** Desde dónde se conectó.
- **Resultado:** `SUCCESS` o `FAILURE` (con el motivo).

## 3. Integridad del Audit Trail
Un rastro de auditoría que se puede borrar no sirve de nada.
- **Storage Externo:** Envía los logs de auditoría a un sistema fuera de la DB principal (ej: AWS CloudWatch Logs, SIEM).
- **Inmutabilidad:** Configura el almacenamiento para que el backend pueda escribir (`append`) pero nunca editar ni borrar registros pasados.

## 4. Auditoría para el Usuario (Historial)
Muchos sistemas senior ofrecen al usuario un "Historial de actividad".
- **Concepto:** Ayuda al usuario a detectar si alguien ha entrado en su cuenta ("Inicios de sesión desde una nueva ubicación").

## 5. Auditoría de Base de Datos
Usa triggers en la DB o librerías como `SQLAlchemy-Continuum` para guardar una copia de cada fila antes de ser modificada. Esto permite hacer "viajes en el tiempo" para ver quién cambió un precio o un estado hace 3 meses.

## Resumen: Responsabilidad y Transparencia
Un sistema de auditoría robusto es tedioso de implementar pero es tu mejor aliado ante un incidente de seguridad. Te permite reconstruir los hechos con precisión forense y demostrar que tu sistema cumple con las normativas vigentes.
