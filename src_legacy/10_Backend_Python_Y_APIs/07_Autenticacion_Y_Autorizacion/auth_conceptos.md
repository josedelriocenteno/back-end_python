# Autenticación vs Autorización: Los dos pilares de la seguridad

En el desarrollo backend, confundir estos dos términos es un error de principiante. Un sistema seguro debe manejar ambos de forma independiente pero coordinada.

## 1. Autenticación (AuthN): ¿Quién eres?
Es el proceso de verificar la identidad de un usuario. Es el "DNI" o "Pasaporte" del mundo digital.
*   **Métodos comunes:**
    *   **Algo que sabes:** Password, PIN.
    *   **Algo que tienes:** Token físico, App de autenticación (2FA).
    *   **Algo que eres:** Huella dactilar, cara (Biometría).
*   **En APIs:** Generalmente usamos el Header `Authorization`.

## 2. Autorización (AuthZ): ¿Qué puedes hacer?
Una vez que sabemos quién eres, debemos decidir a qué tienes permiso.
*   **Ejemplo:** Juan está autenticado, pero Juan es un "Editor", por lo tanto no está autorizado para "Borrar la base de datos".
*   **Niveles de Autorización:**
    *   **Basada en Roles (RBAC):** Admin, Editor, User.
    *   **Basada en Atributos (ABAC):** Solo puedes editar este documento si tú eres el dueño.
    *   **Basada en Permisos (Scopes):** El cliente tiene permiso `read:users` pero no `write:users`.

## 3. El flujo profesional: OAuth2 y OpenID Connect
*   **OAuth2:** Es un estándar de **Autorización**. Permite que una aplicación acceda a datos de otra sin compartir la contraseña.
*   **OpenID Connect (OIDC):** Es una capa sobre OAuth2 que añade **Autenticación**.

## 4. Stateless Authentication (Tokens)
En REST, como no guardamos sesión en el servidor, usamos Tokens (específicamente JWT).
1.  El usuario envía credenciales.
2.  El servidor valida y devuelve un **Token firmado**.
3.  El cliente guarda el token y lo envía en cada petición subsiguiente.
4.  El servidor valida la firma del token sin mirar la DB (¡ahorro de rendimiento!).

## 5. El principio de "Least Privilege" (Menor Privilegio)
Un usuario o servicio solo debe tener los permisos mínimos estrictamente necesarios para cumplir su función. Un script de backup solo necesita leer la DB, no necesita borrar usuarios.

## Resumen: La Puerta y el Pasillo
La autenticación es la **puerta** de tu edificio (te deja entrar). La autorización es el **pasillo** y las puertas de las habitaciones (te dice a dónde puedes ir). En un backend senior, los middlewares validan la puerta y las dependencias validan el pasillo.
