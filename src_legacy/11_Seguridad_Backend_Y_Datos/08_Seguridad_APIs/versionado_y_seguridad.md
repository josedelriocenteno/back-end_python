# Versionado y Seguridad: No dejes a nadie atrás

El versionado de una API (`/v1/`, `/v2/`) no es solo una cuestión de organización, es una decisión de seguridad crítica. Los sistemas antiguos suelen ser los más vulnerables.

## 1. El peligro de las "Versiones Fantasma"
Es común mantener `/v1/` para no romper clientes antiguos.
- **Riesgo:** Si encuentras un fallo de seguridad y solo lo arreglas en `/v2/`, la versión `/v1/` se convierte en una puerta trasera permanente para los atacantes.
- **Regla de Oro:** Si un bug es de seguridad, DEBE ser corregido en todas las versiones activas de la API simultáneamente.

## 2. Políticas de Deprecación (Sunsetting)
Debes avisar a tus usuarios con antelación de que una versión va a morir.
- **Header `Sunset`:** Un estándar (RFC 8594) para indicar cuándo una versión dejará de funcionar.
- **Header `Link`:** Para enviar a los usuarios a la documentación de la nueva versión.

## 3. Seguridad en el Versionado por Header
Algunas APIs usan `Accept: application/vnd.myapi.v2+json`. 
- **Ventaja:** URLs limpias.
- **Riesgo:** Es más fácil de saltarse o de olvidar en las configuraciones de seguridad del Firewall/WAF, que suelen basarse en la ruta (path).

## 4. Breaking Changes y Seguridad
A veces, mejorar la seguridad *rompe* la API (ej: obligar a usar un nuevo header de seguridad).
- **Decisión Senior:** Es preferible romper una integración antigua que dejar a tus usuarios expuestos. Pero hazlo mediante una nueva versión para dar tiempo a la migración.

## 5. Inventario de Endpoints
Usa herramientas para saber qué tanto se usa cada versión. Si nadie ha llamado a `/v1/` en los últimos 30 días, apágala inmediatamente para reducir la superficie de ataque.

## Resumen: Menos es más fuerte
Cuantas más versiones de tu API mantengas encendidas, más difícil es asegurar el sistema. Aspira a tener máximo 2 versiones activas al mismo tiempo y sé agresivo (pero comunicativo) cerrando las antiguas.
