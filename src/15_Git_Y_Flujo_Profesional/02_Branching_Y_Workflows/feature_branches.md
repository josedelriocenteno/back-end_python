# Feature Branches: Desarrollo aislado y limpio

El patrón de "Feature Branch" es la base de la colaboración moderna en equipos de software.

## 1. Un cambio = Una rama
Nunca trabajes directamente sobre `main`. 
1. Crea una rama para tu tarea específica (`feature/login-system`).
2. Haz todos tus commits ahí.
3. Cuando termines, intégrala en la rama principal.

## 2. Nomenclatura Recomendada
Usa prefijos para que el equipo sepa qué tipo de tarea estás haciendo:
- `feature/nombre`: Funcionalidad nueva.
- `bugfix/nombre`: Arreglo de error.
- `hotfix/nombre`: Arreglo urgente en producción.
- `refactor/nombre`: Mejora de código existente.

## 3. Integración básica: Merge
Cuando tu rama está lista, vuelves a la principal y la fusionas.
```bash
git checkout main
git merge feature/mi-mejor-codigo
```

## 4. Borrado Post-Merge
Una vez que el código está en `main`, la rama ya no sirve para nada (el historial de commits ya ha pasado a la rama destino).
```bash
git branch -d feature/mi-mejor-codigo
```

## 5. El beneficio del Contexto
Si trabajas en ramas separadas, puedes pivotar entre tareas instantáneamente. 
- Te piden un cambio urgente mientras haces el login -> Stash -> Checkout main -> Crear hotfix -> Merge -> Volver a tu login. Todo sin mezclar código a medio hacer.

## Resumen: Limpieza Total
Las Feature Branches mantienen el código estable a salvo. Permiten que el flujo de trabajo sea organizado y que las revisiones de código (Pull Requests) sean mucho más sencillas de gestionar.
