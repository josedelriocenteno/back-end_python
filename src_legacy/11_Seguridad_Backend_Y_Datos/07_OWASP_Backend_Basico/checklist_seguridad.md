# Checklist de Seguridad: Antes de ir a Producción

No te fíes de tu memoria. Antes de hacer el despliegue final, verifica cada uno de estos puntos. Si falta uno, la App NO es segura.

## 🛡️ Autenticación y Sesión
- [ ] ¿Las contraseñas se hashean con Bcrypt/Argon2?
- [ ] ¿Los JWT tienen una expiración corta (< 1 hora)?
- [ ] ¿Los Refresh Tokens son rotativos o revocables en DB?
- [ ] ¿Se genera un nuevo Session ID tras el login?
- [ ] ¿El `SECRET_KEY` es largo, aleatorio y está en el Secret Manager?

## 🚪 Autorización
- [ ] ¿Cada endpoint verifica el Rol o Permiso del usuario?
- [ ] ¿Se valida que el usuario es dueño del ID que intenta editar/borrar (IDOR)?
- [ ] ¿Hay una política de "Denegar por defecto"?

## 🔍 Datos y Base de Datos
- [ ] ¿Todas las queries son parametrizadas (sin f-strings)?
- [ ] ¿Los datos sensibles (DNI, IBAN) están cifrados en reposo?
- [ ] ¿El usuario de la DB tiene permisos mínimos (no es root)?
- [ ] ¿Se han desactivado los mensajes de error detallados del motor de DB?

## 🌐 API e Infraestructura
- [ ] ¿Está configurado el Rate Limiting?
- [ ] ¿CORS está configurado con orígenes específicos (no '*')?
- [ ] ¿Están presentes los headers de seguridad (X-Frame, CSP)?
- [ ] ¿Se ha desactivado Swagger/Docs en el entorno de producción?
- [ ] ¿La conexión es 100% HTTPS mediante HSTS?

## 📝 Auditoría
- [ ] ¿Se loguean los intentos de acceso fallidos?
- [ ] ¿Los logs están limpios de contraseñas y tokens?
- [ ] ¿Se han escaneado las dependencias en busca de CVEs (safety/snyk)?

---

## El veredicto final
Si has marcado todos los puntos, felicidades: tienes un backend de nivel profesional. Si te falta alguno, tienes una "deuda técnica de seguridad" que debes pagar antes de que lo haga un atacante por ti.
