# Principios Fundamentales de Seguridad Backend

Para no perderse en la infinidad de parches y configuraciones, un desarrollador debe guiarse por principios universales. Estos principios son la "brújula" que te dirá si un diseño es seguro o no.

## 1. Mínimo Privilegio (Least Privilege)
**Dar solo el permiso estrictamente necesario para cumplir una tarea, durante el tiempo mínimo necesario.**
- **Ejemplo en Backend:** El usuario `app_user` que usa tu API para conectar con la base de datos no debe ser el `owner` de la DB. No debería tener permisos para borrar tablas, solo para hacer `SELECT`, `INSERT` y `UPDATE` en las tablas de su dominio.

## 2. Defensa en Profundidad (Defense in Depth)
**No confíes en que una sola medida de seguridad sea infalible. Crea múltiples capas.**
- **Ejemplo:**
    1. El Firewall bloquea IPs maliciosas.
    2. Nginx tiene Rate Limiting.
    3. FastAPI valida el Token JWT.
    4. El Servicio valida si el recurso pertenece al usuario.
    5. La Base de Datos tiene permisos restringidos.
Si una capa falla, las demás siguen protegiendo el sistema.

## 3. Seguridad por Oscuridad (Security by Obscurity)
**OCULTAR cómo funciona algo NO es seguridad. La seguridad debe residir en el diseño, no en el secreto del mecanismo.**
- **Mala práctica:** Crear un endpoint secreto `/api/super-secret-admin-1234` esperando que nadie lo adivine.
- **Buena práctica:** Tener un endpoint `/api/admin` protegido con una autenticación robusta y multifactor.

## 4. Fail Securely (Falla de forma segura)
**Cuando un sistema falla, debe hacerlo en el estado más restrictivo posible.**
- **Ejemplo:** Si tu código de validación de permisos lanza una excepción inesperada (bug), la respuesta por defecto debe ser "Acceso Denegado", no permitir el acceso porque "el control de permisos se ha roto".

## 5. Economía de Mecanismos (Simplicidad)
**Cuanto más complejo es un sistema de seguridad, más probable es que tenga errores o "puertas traseras" accidentales.** Mantén tu lógica de permisos sencilla de leer y de testear.

## 6. Separación de Responsabilidades (Separation of Concerns)
No mezcles lógica de negocio con lógica de seguridad si puedes evitarlo.
- **Aplicación:** Usa middlewares o decoradores para la seguridad. Así el código de tu función de "Crear Factura" se centra en facturas, no en validar tokens.

## Resumen: La mentalidad del Arquitecto Seguro
Adoptar estos principios hará que tus discusiones técnicas suban de nivel. En lugar de decir "deberíamos añadir un if aquí", dirás "estamos violando el principio de defensa en profundidad aquí". Es la base del pensamiento Senior.
