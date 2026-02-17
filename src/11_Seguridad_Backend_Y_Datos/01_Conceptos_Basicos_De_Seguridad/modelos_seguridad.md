# Modelos de Control de Acceso: RBAC, ABAC y Scopes

Una vez que has decidido implementar la autorización, debes elegir el modelo que mejor se adapte a la complejidad de tu aplicación.

## 1. RBAC (Role-Based Access Control)
Es el modelo más común y sencillo. Los permisos se asignan a **Roles**, y los usuarios se asignan a Roles.
- **Ejemplo:**
    - Rol `Editor`: Puede crear y editar posts.
    - Rol `Viewer`: Solo puede leer posts.
- **Ventaja:** Muy fácil de entender y de implementar con tablas simples en la DB o claims en el JWT.

## 2. ABAC (Attribute-Based Access Control)
Es el modelo más avanzado y flexible. El acceso se decide evaluando una serie de atributos del usuario, del recurso y del entorno.
- **Lógica:** "Un usuario puede EDITAR un DOCUMENTO si (Usuario.rol == Editor) Y (Documento.departamento == Usuario.departamento) Y (Es_horario_laboral == True)".
- **Ventaja:** Permite políticas de seguridad extremadamente granulares.

## 3. Basado en Scopes (OAuth2 / Scopes)
Común en APIs que son consumidas por otras aplicaciones (no solo usuarios). Define "niveles de acceso" que el usuario concede a la aplicación.
- **Ejemplo:** Una App de analítica me pide permiso de `read:stats`. Yo se lo concedo, pero eso no le da permiso para `write:profile` aunque yo, como usuario, sí tenga ese permiso.
- **Concepto Clafe:** Los scopes limitan lo que la *aplicación* puede hacer, no necesariamente lo que el *usuario* puede hacer.

## 4. ReBAC (Relationship-Based Access Control)
Ganando mucha popularidad gracias a sistemas como Google Zanzibar. El acceso se basa en la relación directa entre el usuario y el recurso.
- **Ejemplo:** "Juan puede ver la Carpeta A porque Juan es HERMANO de Pedro y Pedro es DUEÑO de la Carpeta A". (Permisos por grafos de relaciones).

## 5. ¿Cuál elegir?
- **Proyectos Pequeños/Medianos:** RBAC es suficiente y el estándar de la industria.
- **Sistemas Corporativos Complejos:** ABAC o Scopes son necesarios para manejar jerarquías y condiciones variables.
- **Redes Sociales / Apps Colaborativas:** ReBAC es el rey.

## Resumen: Escalabilidad de Permisos
Elegir el modelo correcto al principio te ahorrará meses de refactorización. RBAC suele ser el punto de partida, pero asegúrate de que tu arquitectura permite evolucionar hacia modelos más complejos si el negocio lo requiere.
