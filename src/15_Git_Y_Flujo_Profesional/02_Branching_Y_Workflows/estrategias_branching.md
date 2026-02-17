# Estrategias de Branching: Protocolos de equipo

Tener ramas es solo el principio. Acordar cómo usarlas es lo que hace que el equipo no pierda el tiempo resolviendo conflictos inútiles.

## 1. Sincronización Diaria
Incluso si tu rama dura 5 días, debes traer los cambios de `main` **todos los días**.
- **Comando:** `git fetch origin` seguido de `git merge origin/main`.
- **Beneficio:** Si alguien cambia algo que afecta a tu código, lo verás hoy, no el viernes minutos antes del despliegue.

## 2. Ramas de Larga Duración
Evítalas. Una rama de más de 1 semana es un imán de conflictos de merge.
- **Tip Senior:** Si una funcionalidad es muy grande, divídela en "sub-features" más pequeñas que puedan integrarse de forma independiente.

## 3. Propiedad del Código
En algunos equipos, solo ciertas personas (Maintainers) pueden mergear en `main`. Las ramas de feature son "terreno libre" del desarrollador, pero `main` es terreno sagrado del equipo.

## 4. Protección de Ramas (Branch Protection)
Configura en GitHub que la rama `main`:
- No permita `push` directos.
- Requiera que los Tests de CI pasen.
- Requiera al menos 1 aprobación (Review) de un compañero.

## 5. El coste del desvío
Cuantos más commits de diferencia haya entre tu rama y `main`, más difícil y arriesgado será el merge. Integrar cambios pequeños a menudo es mucho más seguro que integrar un cambio gigante rara vez.

## Resumen: Comunicación Continua
Git es una herramienta técnica que resuelve un problema de comunicación. Ninguna estrategia de ramas sustituye a una buena charla con el equipo sobre quién está tocando qué.
