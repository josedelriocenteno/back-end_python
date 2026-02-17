# Rebase Interactivo: El bisturí del historial

¿Has hecho 5 commits de "fix typo", "arreglo test" y "ups"? El rebase interactivo permite "aplastar" esos commits y dejar una historia limpia y profesional.

## 1. El comando mágico
`git rebase -i HEAD~N` (donde N es el número de commits que quieres revisar).

## 2. El Menú de Opciones
Se abrirá un editor con una lista de commits precedidos por la palabra `pick`. Puedes cambiar `pick` por:
- `reword`: Mantener el commit pero cambiar el mensaje.
- `edit`: Parar para hacer cambios en el código de ese commit.
- `squash`: Fusionar el commit con el de arriba (combina mensajes).
- `fixup`: Como squash, pero descarta el mensaje de este commit (el más usado).
- `drop`: Eliminar el commit por completo.

## 3. Ejemplo Práctico
Supongamos que quieres limpiar tus últimos 3 cambios:
```text
pick a1b2c3d feat: nueva api
fixup e5f6g7h fix: corregido typo en api
fixup i9j0k1l fix: corregido error de importación
```
Al guardar, tendrás **un solo commit** con el mensaje "feat: nueva api" y todo el código combinado.

## 4. Cuándo usarlo
- Justo antes de abrir una Pull Request.
- Para limpiar experimentos fallidos en tu rama local.
- Para reordenar commits si la lógica queda más clara así.

## 5. El peligro de reescribir el pasado
Recuerda: Si ya has hecho `push` a una rama compartida, no hagas rebase interactivo. Estarás cambiando los identificadores de los commits y tus compañeros verán errores extraños.

## Resumen: Presentación Impecable
Un historial limpio facilita el trabajo de los revisores y de cualquiera que tenga que buscar el origen de un error meses después. El rebase interactivo es la herramienta definitiva para lograrlo.
