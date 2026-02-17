# Errores de Seguridad Comunes en Autenticación

Incluso con las mejores librerías, es fácil meter la pata en seguridad. Estos son los fallos que los auditores de seguridad (Pentester) buscan primero.

## 1. Hardcoding de Secretos
*   **Fallo:** Escribir el `SECRET_KEY` directamente en el código o subir el archivo `.env` a GitHub.
*   **Consecuencia:** Si alguien ve tu código, puede fabricar tokens válidos para cualquier usuario (incluyendo el admin).

## 2. JWT sin Expiración
*   **Fallo:** Generar un token con 5 años de duración o simplemente sin el campo `exp`.
*   **Consecuencia:** Si el token es robado, el atacante tiene acceso eterno a la cuenta del usuario.

## 3. Débil Algoritmo de Hashing
*   **Fallo:** Usar MD5 o SHA-1 para contraseñas.
*   **Consecuencia:** Estos algoritmos son tan rápidos que un ordenador moderno puede probar millones de combinaciones por segundo (fuerza bruta).
*   **Solución:** Usa **Bcrypt**, **Argon2** o **Scrypt**. Son lentos a posta para evitar ataques.

## 4. No Invalidar Tokens al Cerrar Sesión (Logout)
*   **Fallo:** El botón de Logout del frontend simplemente borra el token del LocalStorage.
*   **Consecuencia:** El token sigue siendo válido en el servidor. Si el hacker lo copió antes, puede seguir usándolo.
*   **Solución:** Blacklisting de tokens en Redis o uso de Refresh Tokens revocables.

## 5. User Enumeration (Enumeración de Usuarios)
*   **Fallo:** Al fallar el login, decir "La contraseña es incorrecta" o "El usuario no existe".
*   **Consecuencia:** Le estás confirmando al atacante que ese email existe en tu base de datos.
*   **Solución:** Usa siempre un mensaje genérico: "Email o contraseña incorrectos".

## 6. Falta de Rate Limiting en el Login
*   **Fallo:** Permitir 10,000 intentos de login por segundo desde la misma IP.
*   **Consecuencia:** Ataque de fuerza bruta exitoso en cuestión de minutos.

## 7. No Usar HTTPS (SSL)
*   **Fallo:** Enviar tokens o contraseñas por HTTP plano.
*   **Consecuencia:** Ataque Man-in-the-Middle. Cualquier persona en el mismo Wi-Fi público puede ver tus credenciales.

## Resumen: Piensa como un Hacker
La seguridad no es un producto que compras, es un proceso que mantienes. No confíes en que tus usuarios elegirán buenas contraseñas o que sus redes serán seguras. Blinda tu backend asumiendo que el cliente está en un entorno hostil.
