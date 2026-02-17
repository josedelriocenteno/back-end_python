# Reset, Checkout y Revert: ¿Cómo volver atrás?

Saber "deshacer" es tan importante como saber "hacer". Git ofrece tres formas de volver al pasado, y elegir la incorrecta puede ser destructivo.

## 1. Git Checkout (Para archivos sueltos)
`git checkout -- archivo.py` o `git restore archivo.py` (comando moderno).
- **Qué hace:** Descarta tus cambios locales y recupera la versión del último commit.
- **Uso:** Cuando has hecho pruebas que no funcionan y quieres limpiar el archivo rápido.

## 2. Git Reset (Mover el puntero)
Mueve la rama actual a un commit anterior. Existen tres tipos:
- **--soft:** Mueve la rama pero MANTIENE tus cambios en el Staging Area (listos para otro commit).
- **--mixed (default):** Mueve la rama y mantiene los cambios en tu carpeta, pero fuera del Stage.
- **--hard:** Borra todo. Mueve la rama y destruye cualquier cambio no commiteado.
- **REGLA:** Úsalo solo en local.

## 3. Git Revert (El camino seguro para producción)
`git revert <hash>`
- **Qué hace:** Crea un **NUEVO commit** que hace exactamente lo opuesto al commit que quieres anular.
- **Ventaja:** No reescribe la historia. Es el único método seguro si el error ya está subido a `main` y otros desarrolladores tienen ese código.
- **Uso:** "He subido un bug a producción, necesito quitarlo YA sin romper el Git de los demás".

## 4. Tabla Comparativa
| Comando | ¿Crea un commit? | ¿Es destructivo? | ¿Seguro para remotos? |
| :--- | :--- | :--- | :--- |
| **Checkout** | No | Sí (locales) | - |
| **Reset** | No | Sí (en --hard) | No |
| **Revert** | Sí | No | **Sí** |

## Resumen: La cirugía del código
Usa **Reset** para limpiar tu trabajo mientras estás solo. Usa **Revert** en cuanto tu código haya tocado el servidor compartido. Entender esta distinción separa a los desarrolladores Jr de los Sr.
