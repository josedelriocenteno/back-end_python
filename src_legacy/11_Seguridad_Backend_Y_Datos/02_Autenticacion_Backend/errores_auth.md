# Errores Comunes de Autenticación (Anti-patrones)

La autenticación es el front-door de tu casa. Cualquier error aquí deja la llave debajo del felpudo para los atacantes. Estos son los fallos que debes evitar a toda costa.

## 1. Mensajes de Error Informativos (Enumeración)
- **Fallo:** Decir "El usuario no existe" o "La contraseña es incorrecta".
- **Realidad:** Le estás diciendo al atacante que ese email tiene cuenta. Le facilitas el trabajo de adivinar solo la contraseña.
- **Solución:** Di siempre: "Credenciales de acceso incorrectas".

## 2. Session Fixation
- **Fallo:** Mantener el mismo ID de sesión que tenía el usuario como "anónimo" una vez que se loguea.
- **Ataque:** Un hacker te envía un link con un ID de sesión pre-generado. Tú te logueas, y el hacker usa ese mismo ID para entrar en tu cuenta.
- **Solución:** Genera SIEMPRE un nuevo ID de sesión al momento del login exitoso.

## 3. No Forzar Contraseñas Fuertes
- **Fallo:** Permitir contraseñas como `123456` o `password`.
- **Realidad:** Los ataques de diccionario romperán esas cuentas en milisegundos.
- **Solución:** Implementa validación (Pydantic/Regex) que obligue a tener longitud mínima, mayúsculas y símbolos.

## 4. JWT sin Firma Segura (Alg=None)
- **Fallo:** Aceptar tokens donde el campo `alg` es `none`.
- **Ataque:** El atacante modifica el JSON del token a su antojo y el servidor lo da por válido porque no hay firma que comprobar.
- **Solución:** Configura tu librería de JWT para que SOLO acepte algoritmos robustos como `HS256` o `RS256`.

## 5. Falta de Bloqueo tras Reintentos
- **Fallo:** No hacer nada si alguien falla 100 veces el login.
- **Realidad:** Estás invitando a un ataque de fuerza bruta infinito.
- **Solución:** Usa "Account Lockout" (bloquear la cuenta 15 min tras 5 fallos) o mejor aún, usa un CAPTCHA tras el tercer fallo.

## 6. Auth por Parámetro URL
- **Fallo:** Enviar el token o sesión en la URL: `api.com/users?token=abcd`.
- **Realidad:** Las URLs se guardan en el historial del navegador, en los logs del servidor y en los proxys. El token queda expuesto a cualquiera con acceso a esos logs.
- **Solución:** Usa siempre los Headers de HTTP (`Authorization`) o Cookies.

## Resumen: Piensa en el peor escenario
Un buen desarrollador asume que habrá miles mas de atacantes que de usuarios legítimos. Blindar el proceso de login es la tarea más aburrida pero la más vital para la supervivencia del proyecto.
