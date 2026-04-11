# Control de Accesos: Roles y Permisos en el Repositorio

Gestionar quién puede hacer qué en un repositorio es vital para prevenir borrados accidentales o inyección de código malicioso.

## 1. Roles en GitHub
- **Owner:** Control total (ajustes, facturación, borrado del repo).
- **維持者 (Maintainer):** Gestiona el proyecto sin acceso a facturación. Puede mergear PRs y crear releases.
- **Write:** Puede hacer `push` y crear ramas. (El rol estándar para desarrolladores).
- **Triage:** Puede gestionar labels e issues pero no tiene acceso al código.
- **Read:** Solo lectura. Ideal para auditores o perfiles de producto que solo quieren ver el progreso.

## 2. Ramas Protegidas (Branch Protection Rules)
Es la defensa más importante para `main`.
- **Require PR before merging:** Nadie puede subir código a main directamente.
- **Require Status Checks:** El merge solo se habilita si los tests de CI han pasado.
- **Restrict Pushes:** Solo los Leads pueden autorizar el merge final.

## 3. CODEOWNERS: El archivo de responsabilidad
Puedes crear un archivo en `.github/CODEOWNERS` indicando quién es responsable de cada carpeta.
```text
# Los leads revisan todo
*       @team-leads

# Los expertos en DB revisan las migraciones
/db/    @database-experts

# Los de seguridad revisan la carpeta auth
/auth/  @security-officer
```
GitHub solicitará automáticamente la revisión de estas personas cuando se toque esa carpeta.

## 4. Equipos y Organizaciones
No des permisos usuario por usuario. Crea equipos (Backend, Frontend, DevOps) y asigna el equipo al repositorio. Es mucho más fácil de gestionar cuando alguien entra o sale de la empresa.

## 5. Auditoría de Seguridad
Revisa periódicamente quién tiene acceso. Los desarrolladores que ya no están en el proyecto deben ser eliminados inmediatamente (proceso de Offboarding).

## Resumen: El Principio de Menor Privilegio
Solo da a cada persona el acceso mínimo que necesita para hacer su trabajo. Esto reduce la superficie de ataque y previene errores críticos que podrían afectar a la estabilidad del negocio.
