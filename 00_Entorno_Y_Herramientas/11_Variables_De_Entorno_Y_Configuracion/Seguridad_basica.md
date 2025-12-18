# Seguridad Básica en Backend Python

## 1. Introducción

La seguridad básica en backend Python es **fundamental desde el primer día**.  
No solo protege datos sensibles y credenciales, sino que también garantiza que el proyecto sea confiable y profesional.  
Se basa en **buenas prácticas de código, configuración y manejo de datos**.

> ⚠️ Nota:
> Seguridad no es un añadido; es parte integral de todo flujo de desarrollo profesional.

---

## 2. Principios de seguridad profesional

1. **Separación de código y configuración**  
   - Credenciales y secretos nunca en el código.  
   - Uso de `.env` y archivos de configuración por entorno.  

2. **Principio de menor privilegio**  
   - Servicios y usuarios con permisos estrictamente necesarios.  

3. **Validación y saneamiento de datos**  
   - Siempre validar inputs de usuario para prevenir inyecciones SQL, XSS y ataques similares.  

4. **Uso de HTTPS y cifrado**  
   - Toda comunicación sensible debe estar cifrada con TLS.  

5. **Autenticación y hashing de contraseñas**  
   - Nunca almacenar contraseñas en texto plano.  
   - Uso de librerías como `bcrypt` o `argon2`.

---

## 3. Buenas prácticas en manejo de credenciales

```python
from dotenv import load_dotenv
import os
from passlib.hash import bcrypt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Hash de contraseñas
hashed_password = bcrypt.hash("contraseña_segura")
assert bcrypt.verify("contraseña_segura", hashed_password)
Nunca hardcodear secretos.

Validar que variables críticas estén definidas al inicio.

4. Validación de inputs
Evitar inyecciones SQL usando ORMs (SQLAlchemy) o consultas parametrizadas.

python
Copiar código
# Correcto: consultas parametrizadas
session.execute("SELECT * FROM users WHERE username=:username", {"username": input_username})
Sanitizar inputs de usuarios en formularios y APIs.

Validar tipos y formatos de datos (email, fechas, números, etc.).

5. Seguridad en dependencias
Revisar vulnerabilidades con herramientas profesionales:

bash
Copiar código
pip install pip-audit
pip-audit
Mantener dependencias actualizadas (pip list --outdated).

Evitar paquetes de fuentes no confiables.

6. Manejo de errores y logs
Nunca mostrar stack traces o errores internos al usuario final.

Loguear errores de forma segura y centralizada (sin exponer secretos).

python
Copiar código
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Usuario autenticado correctamente")
logging.error("Error al conectar a la base de datos")  # sin mostrar contraseñas
7. Buenas prácticas profesionales adicionales
Configurar roles y permisos de manera estricta en bases de datos y APIs.

Usar tokens JWT o sistemas de autenticación seguros.

Revisar y auditar configuraciones de seguridad periódicamente.

Integrar validaciones y seguridad en tests automatizados.

Documentar y comunicar políticas de seguridad en el equipo.

8. Errores comunes a evitar
Hardcodear claves o contraseñas.

No validar inputs de usuario.

Ignorar vulnerabilidades de dependencias.

Exponer información sensible en logs o errores.

Dar permisos excesivos a servicios o usuarios.

9. Checklist rápido
 Código y configuración separada

 Variables de entorno con secretos gestionadas correctamente

 Contraseñas hasheadas, nunca en texto plano

 Inputs de usuario validados y sanitizados

 Dependencias auditadas y actualizadas

 Logs y errores manejados de forma segura

 Roles y permisos correctamente configurados

10. Conclusión
Implementar seguridad básica profesional desde el inicio es clave para proyectos backend Python.
Permite prevenir vulnerabilidades, proteger datos y generar confianza en usuarios y equipos.
La seguridad debe estar integrada en código, configuración, dependencias y flujos de trabajo diarios.