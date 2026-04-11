# Stash Profesional: Guardar trabajo temporal

El "Cajón de Sastre" de Git es mucho más que un simple comando global. Dominar el Stash te permite gestionar múltiples urgencias al mismo tiempo.

## 1. Guardar con Nombre
No hagas simplemente `git stash`. Ponle descripción para saber qué hay dentro.
`git stash save "trabajo a medias en el login"` o `git stash push -m "mensaje"`

## 2. Listar e Inspeccionar
`git stash list` - Muestra todos tus stashes numerados (`stash@{0}`, `stash@{1}`).
`git stash show -p stash@{0}` - Mira exactamente qué cambios hay guardados sin sacarlos.

## 3. Incluir archivos nuevos (Untracked)
Por defecto, `git stash` solo guarda archivos que Git ya conoce. Si has creado archivos nuevos, usa:
`git stash -u` (include-untracked).

## 4. Sacar del cajón
- `git stash pop`: Saca el último cambio (`stash@{0}`) y lo **borra** de la lista.
- `git stash apply`: Saca el cambio pero lo **mantiene** en la lista (por si acaso algo falla).

## 5. Convertir un Stash en una Rama
Si el trabajo que guardaste "un momento" ha crecido y ahora quieres dedicarle una rama propia:
`git stash branch nombre-de-la-rama stash@{0}`
Git creará la rama, aplicará los cambios y borrará el stash.

## Resumen: Pausa inteligente
El Stash es tu mejor aliado cuando te interrompen. Úsalo para mantener tu espacio de trabajo limpio y organizado sin necesidad de hacer "commits basura" con títulos como "cambios temporales".
