# Autenticación vs Autorización: La distinción definitiva

Como vimos brevemente en el tema anterior, estos son los cimientos de cualquier sistema de seguridad. Vamos a profundizar en los matices técnicos que todo desarrollador senior debe dominar.

## 1. Autenticación (¿Quién eres?)
Es el proceso de verificar una declaración de identidad.
- **Mecanismos:** 
    - **Password hashing:** El servidor no guarda tu contraseña, guarda un hash. Al entrar, compara el hash de lo que envías con el guardado.
    - **Multi-Factor (MFA):** Añade capas adicionales (SMS, TOTP, Email).
    - **Identidad Federada:** "Login with Google/GitHub" (OIDC).
- **Resultado:** Un identificador único de usuario (User ID) que el sistema ahora reconoce como "Válido".

## 2. Autorización (¿Qué puedes hacer?)
Es el proceso de decidir si un usuario autenticado tiene permiso para una acción específica.
- **Mecanismos:**
    - **Control de Acceso basado en Roles (RBAC):** Admin, Editor, Viewer.
    - **Control de Acceso basado en Atributos (ABAC):** "Solo si es mayor de 18 Y el documento está en estado BORRADOR".
    - **Listas de Control de Acceso (ACL):** Una lista ligada a cada recurso con quién puede leerlo o escribirlo.
- **Resultado:** Un "SÍ" o un "NO" (403 Forbidden).

## 3. Comparativa Técnica

| Característica | Autenticación | Autorización |
| :--- | :--- | :--- |
| **Pregunta** | ¿Quién eres? | ¿Tienes permiso? |
| **Momento** | Al inicio de la sesión / Cada request | Después de la autenticación |
| **Error (HTTP)** | 401 Unauthorized | 403 Forbidden |
| **Ejemplo** | Introducir usuario y contraseña | Intentar borrar un post de otro usuario |

## 4. El peligro de la confusión
Un error común es devolver un **401** cuando un usuario está logueado pero intenta acceder a algo prohibido.
- **Correcto:** Si el usuario está identificado pero no tiene permisos, devuelve **403**. El 401 le dice al frontend "Vuelve a loguearte", el 403 le dice "No tienes derecho a estar aquí".

## 5. Delegación de Autorización (OAuth2)
Este es un nivel avanzado. OAuth2 permite que un tercero (una App de móviles) actúe en nombre del usuario sin conocer su contraseña. Aquí la autorización se maneja mediante **Scopes** (alcances), por ejemplo: `read:profile`, `write:tweets`.

## Resumen: Independientes pero coordinados
Aunque son procesos distintos, suelen viajar juntos en el backend. Un middleware de autenticación identifica al usuario y lo inyecta en el objeto `request`, y luego un decorador de autorización consulta ese objeto para validar si la operación está permitida.
