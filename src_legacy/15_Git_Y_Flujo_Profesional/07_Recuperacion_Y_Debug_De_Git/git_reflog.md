# Git Reflog: La caja negra del repositorio

¿Has hecho un `reset --hard` por error? ¿Has borrado una rama antes de subirla? No entres en pánico. El **Reflog** es el historial de todos los movimientos que ha hecho el puntero `HEAD` en tu máquina.

## 1. El concepto
Git guarda un registro de cada vez que el "foco" (HEAD) cambia de lugar, ya sea por un commit, un checkout, un merge o un reset. Este historial vive solo en tu ordenador y no se sube a GitHub.

## 2. Cómo usarlo
```bash
git reflog
```
Verás una lista como esta:
- `df2a7b1 HEAD@{0}: reset: moving to HEAD~1`
- `a1b2c3d HEAD@{1}: commit: feat: añadida api`

## 3. Rescatar un commit perdido
Si quieres volver al estado justo antes del desastre (en este caso, `HEAD@{1}`):
`git reset --hard a1b2c3d` o `git reset --hard HEAD@{1}`.

## 4. Diferencia con `git log`
- **git log:** Es el historial de commits de la rama. Si borras un commit o una rama, desaparece del log.
- **git reflog:** Es el historial de tus acciones. Aunque borres la rama, el movimiento del HEAD sigue registrado durante 30-90 días.

## 5. Limpieza automática
Git limpia el reflog periódicamente para no ocupar espacio infinito. No esperes 3 meses para intentar recuperar un código borrado.

## Resumen: Nada se pierde realmente
Para un desarrollador profesional, el `reflog` es la red de seguridad definitiva. Saber que casi cualquier desastre local se puede deshacer te da la calma necesaria para trabajar con herramientas potentes como el rebase.
