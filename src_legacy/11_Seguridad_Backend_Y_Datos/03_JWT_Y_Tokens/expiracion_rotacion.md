# Expiración y Rotación de Tokens

Configurar los tiempos de expiración y las reglas de rotación es donde se define el equilibrio entre seguridad y comodidad. No existe un valor perfecto, sino una estrategia adecuada para cada tipo de aplicación.

## 1. Estrategia de Expiración
- **Aplicación Bancaria/Crítica:**
    - Access: 5 minutos.
    - Refresh: 1 hora.
    - Logout automático por inactividad.
- **Red Social / App Consumo:**
    - Access: 1 hora.
    - Refresh: 30 días.
- **Herramienta de Trabajo (SaaS):**
    - Access: 30 minutos.
    - Refresh: 7 días.

## 2. Rotación de Refresh Tokens (RTR)
Es el mecanismo donde cada vez que pides un nuevo Access Token usando un Refresh Token, el servidor te da otro Refresh Token NUEVO e invalida el anterior.
- **Ventaja de Detección:** Si un atacante roba un Refresh Token y lo usa, y luego el usuario real intenta usar su token viejo, el servidor verá que el mismo token se ha usado dos veces. Esto es señal de hackeo. El servidor puede entonces **invalidar TODOS los tokens** de ese usuario para obligarlo a re-autenticarse.

## 3. ¿Dónde guardar la lógica de expiración?
- El backend decide la duración y la firma en el token (`exp`).
- El frontend debe ser inteligente: detectar que el token va a caducar e intentar el refresco *antes* de que la petición del usuario falle.

## 4. El peligro de 'Remember Me'
Muchos sistemas permiten sesiones de meses con el botón "Recordarme".
- **Fallo:** Dejar un Access Token válido por meses.
- **Correcto:** Dejar un Refresh Token válido por meses, pero con auditoría constante de si se está usando desde el mismo dispositivo/ciudad.

## 5. Parámetros de seguridad extra
- **iat (Issued At):** Cuándo se creó el token. Útil para invalidar todos los tokens creados antes de que el usuario reseteara su contraseña.
- **nbf (Not Before):** El token no es válido hasta esta fecha futura (poco común pero útil para planes de suscripción).

## Resumen: Los tokens no son eternos
Configurar expiraciones cortas es molesto para los desarrolladores durante los tests, pero es el seguro de vida más barato para tus usuarios en producción. Aplica rotación siempre que puedas para detectar intrusiones de forma proactiva.
