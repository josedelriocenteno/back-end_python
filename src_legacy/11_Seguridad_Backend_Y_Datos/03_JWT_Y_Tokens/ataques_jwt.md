# Ataques Comunes a JWT: Cómo evitar que rompan tu API

Los tokens JWT no son mágicos; tienen debilidades conocidas si se implementan o gestionan mal. Aquí están los ataques que un Pentester intentará contra tu backend.

## 1. Algorithmic Switching (El ataque `none`)
- **Fallo:** La librería permite que el atacante cambie el header `"alg": "HS256"` por `"alg": "none"`.
- **Resultado:** El servidor deja de verificar la firma y acepta el token tal cual.
- **Protección:** NUNCA permitas el algoritmo `none` en tu configuración. Usa librerías modernas que bloqueen esto por defecto.

## 2. Inyección de Claims (Escalada de Privilegios)
- **Fallo:** El atacante descodifica el token (que es público), cambia `"rol": "user"` por `"rol": "admin"` y lo envía de vuelta.
- **Protección:** La firma detectará el cambio de un solo bit en el JSON y el token será rechazado. La seguridad de JWT reside en que el atacante no tiene tu `SECRET_KEY` para generar una firma nueva válida.

## 3. Fuerza Bruta sobre el Secret Key
- **Fallo:** Usar un secreto débil como `12345` o `secreto`.
- **Resultado:** Herramientas como `hashcat` pueden probar millones de firmas por segundo hasta encontrar tu clave privada. Una vez la tienen, son dueños de tu API.
- **Protección:** Usa una cadena larga, aleatoria y cámbiala periódicamente.

## 4. Captura de Tokens (Side-channel)
- **Fallo:** El token aparece en los logs del servidor, en el historial del proxy o se envía por HTTP plano.
- **Protección:** Usa HTTPS siempre y trata a los tokens como si fueran oro. Enmascara su valor en los logs.

## 5. Replay Attack (Ataque de Repetición)
- **Fallo:** Si interceptan un token válido, pueden mandarlo mil veces.
- **Protección:** Tiempos de expiración cortos y uso de TLS (HTTPS) para que la interceptación sea casi imposible.

## 6. Confusion RS256 / HS256
- **Ataque:** El atacante intenta usar la clave pública de un algoritmo asimétrico (RS256) como si fuera la clave privada de uno simétrico (HS256).
- **Protección:** Asegúrate de que tu backend espera un solo tipo de clave y algoritmo predefinido.

## Resumen: La Ley de la Selva
Internet es un lugar hostil. Implementar JWT sin conocer estos ataques es como salir a la calle con una cartera abierta. Configura bien tu librería, usa secretos fuertes y nunca, jamás, permitas el algoritmo `none`.
