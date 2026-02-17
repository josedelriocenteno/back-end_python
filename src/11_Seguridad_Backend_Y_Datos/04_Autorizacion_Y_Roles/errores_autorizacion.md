# Errores Comunes de Autorización (AuthZ Failures)

Incluso con un sistema RBAC brillante, las grietas en la lógica de autorización son la causa número uno de filtraciones de datos masivas. Estos son los fallos que debes buscar con lupa.

## 1. Fallo en el "Fallback" (Whitelist vs Blacklist)
- **Fallo:** Permitir el acceso por defecto y prohibirlo en rutas específicas. (Blacklist).
- **Consecuencia:** Si creas una ruta nueva y olvidas protegerla, queda abierta al mundo.
- **Solución (Whitelist):** Deniega el acceso por defecto a TODO y abre permisos explícitamente solo donde sea necesario.

## 2. Ignorar el Verbo HTTP
- **Fallo:** Proteges el `GET /users` pero olvidas proteger el `POST` o el `DELETE` del mismo recurso.
- **Resultado:** Cualquiera puede borrar usuarios aunque no pueda listarlos.

## 3. Confiar en Ocultar IDs (Security by Obscurity)
- **Fallo:** Usar UUIDs largos en lugar de IDs secuenciales pensando que "nadie los adivinará".
- **Realidad:** Si un UUID se filtra en un log o en una URL compartida, el recurso queda desprotegido. Los UUIDs ayudan a la privacidad, NO sustituyen a la autorización.

## 4. Broken Function Level Authorization
- **Fallo:** Un usuario normal puede llamar a funciones internas de la API (como `/api/admin/reset-cache`) porque el desarrollador pensó que "como no está el botón en el frontend, nadie lo llamará".
- **Solución:** Cada endpoint, sin excepción, debe validar los permisos del llamante.

## 5. Falta de Validación de Propiedad (IDOR)
- **Fallo:** Modificar un registro enviando un ID diferente en el body del que hay en la URL, y el backend no comprueba si el usuario es dueño de ese nuevo ID.
- **Solución:** Valida siempre la relación entre el usuario y el recurso que se intenta modificar.

## 6. Permisos "Pegajosos" (Sticky Permissions)
- **Fallo:** El usuario tiene permisos en un JWT que dura 24 horas. Le quitas el rol de Admin en la DB, pero él sigue siendo Admin durante 24 horas más hasta que el token caduque.
- **Solución:** Tiempos de expiración cortos o listas negras para cambios de roles críticos.

## Resumen: La paradoja del permitidor
La autorización es difícil porque es silenciosa. Un error en el código normal hace que algo no funcione (fácil de ver). Un error en la autorización hace que algo funcione DEMASIADO (difícil de detectar). Testea tus permisos tan rigurosamente como tu lógica de negocio.
