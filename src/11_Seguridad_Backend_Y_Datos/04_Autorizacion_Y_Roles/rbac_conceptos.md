# RBAC (Role-Based Access Control): El Estándar de la Industria

RBAC es la forma más efectiva de gestionar permisos en aplicaciones que van desde pequeñas startups hasta grandes corporaciones. La clave es desacoplar al **Usuario** de sus **Permisos** mediante el concepto de **Rol**.

## 1. La Jerarquía RBAC
- **Permisos:** La unidad mínima de acción (ej: `create_user`, `delete_post`).
- **Roles:** Un conjunto de permisos (ej: `admin` tiene todos, `editor` solo algunos).
- **Usuarios:** Se vinculan a uno o varios roles.

## 2. Ventajas del Modelo
- **Facilidad de Gestión:** Si contratas a un nuevo editor, solo le asignas el rol `editor`. No tienes que darle individualmente 50 permisos diferentes.
- **Seguridad por Defecto:** Los nuevos usuarios no tienen roles y, por tanto, no tienen permisos.
- **Auditoría:** Es mucho más fácil auditar "quién tiene el rol admin" que "quién puede borrar la DB".

## 3. Implementación en Base de Datos
Suele requerir 3 tablas principales:
1. `Users` (id, name, ...)
2. `Roles` (id, name, description)
3. `User_Roles` (user_id, role_id) -> Tabla intermedia Many-to-Many.

## 4. RBAC Dinámico vs Estático
- **Estático (Hardcoded):** Los roles están definidos en código (Enums). Es rápido y suficiente para apps sencillas.
- **Dinámico (DB):** Los roles y sus permisos se guardan en la DB y se pueden crear nuevos desde el panel de administración sin tocar el código. Es el nivel Senior real.

## 5. El peligro de la "Explosión de Roles"
Un error común es crear un rol para cada pequeña variación: `editor_junior`, `editor_senior`, `editor_nocturno`.
- **Solución:** Intenta mantener pocos roles base y usa **Scopes** o **Atributos (ABAC)** para las variaciones finas.

## Resumen: Organización del Caos
RBAC no es solo una técnica de programación, es una forma de organizar la seguridad de una empresa. Un sistema RBAC bien diseñado es invisible para el usuario pero un muro infranqueable para un atacante que logre entrar con una cuenta de bajo nivel.
