# Política de Versionado del Proyecto

## 1. Introducción

En cualquier proyecto profesional, **tener una política clara de versionado es fundamental**.  
Permite:

- Controlar cambios y evoluciones del software.  
- Facilitar la colaboración en equipo.  
- Garantizar compatibilidad entre distintas versiones de librerías y aplicaciones.  
- Facilitar despliegues y rollbacks seguros.

> ⚠️ Nota:
> La falta de una política de versionado provoca caos, confusión y errores en producción.

---

## 2. Versionado Semántico (SemVer)

El estándar más usado en proyectos profesionales es **Versionado Semántico (SemVer)**: `MAJOR.MINOR.PATCH`

| Componente | Descripción                                           | Ejemplo                |
|------------|-------------------------------------------------------|-----------------------|
| MAJOR      | Cambios incompatibles que rompen la compatibilidad   | 2.0.0                 |
| MINOR      | Nuevas funcionalidades compatibles con versiones previas | 1.2.0             |
| PATCH      | Corrección de errores sin romper compatibilidad      | 1.2.1                 |

### Reglas de SemVer

1. Incrementar **MAJOR** si hay cambios que rompen la API.  
2. Incrementar **MINOR** si se agregan funcionalidades nuevas sin romper la API.  
3. Incrementar **PATCH** para correcciones de bugs y mejoras menores.  

> 💡 Tip:
> Nunca modificar versiones de forma arbitraria; siempre sigue el SemVer para mantener coherencia.

---

## 3. Versionado Interno del Proyecto

1. **Versiones de desarrollo (`dev`)**  
   - Se usan para testing interno o desarrollo activo.  
   - Ejemplo: `1.2.0-dev.20251218`

2. **Versiones de prueba (`alpha` / `beta`)**  
   - Se usan para QA y pruebas limitadas.  
   - Ejemplo: `1.2.0-beta.1`

3. **Versiones de producción (`release`)**  
   - Estables, documentadas y listas para despliegue.  
   - Ejemplo: `1.2.0`

---

## 4. Estrategias profesionales

- **Etiquetas Git (`tags`)**:  
  - Cada release estable debe tener un tag en Git: `git tag v1.2.0`.  
- **Changelog**:  
  - Mantener un registro de cambios (`CHANGELOG.md`) con las versiones y modificaciones.  
- **Branching model**:  
  - Usar ramas `develop` para desarrollo, `feature/*` para nuevas funcionalidades y `main` para releases estables.  
- **Automatización de versiones**:  
  - Herramientas como `bump2version` o `poetry version` para actualizar versiones automáticamente.

---

## 5. Ejemplo práctico

```bash
# Instalar bump2version
pip install bump2version

# Configurar versión inicial
bump2version --current-version 1.2.0 patch setup.py

# Incrementar PATCH
bump2version patch setup.py  # 1.2.1

# Incrementar MINOR
bump2version minor setup.py  # 1.3.0

# Crear tag en Git para la release
git tag v1.3.0
git push origin v1.3.0
💡 Tip:
Documenta siempre la versión usada en producción en README, Dockerfile y entornos de despliegue.

6. Buenas prácticas de versionado
Seguir SemVer estrictamente.

Mantener el changelog actualizado.

Usar tags Git para cada release.

Separar versiones de desarrollo, prueba y producción.

Automatizar incrementos de versión para evitar errores humanos.

Revisar compatibilidad de dependencias antes de cada release.

7. Checklist rápido
 Política de versionado definida (SemVer)

 Tags Git usados para releases

 Changelog actualizado

 Versiones de desarrollo y pruebas claramente diferenciadas

 Documentación de la versión en README o configuración

 Automatización de incrementos de versión implementada

8. Conclusión
Tener una política de versionado clara y profesional garantiza estabilidad, trazabilidad y confianza en el proyecto.
Permite colaborar de manera eficiente, desplegar sin riesgos y mantener la compatibilidad a lo largo del ciclo de vida del software.