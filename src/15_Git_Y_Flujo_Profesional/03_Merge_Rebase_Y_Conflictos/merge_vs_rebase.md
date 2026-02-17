# Merge vs. Rebase: Diferencias Reales

Ambos comandos sirven para integrar cambios de una rama a otra, pero cambian drásticamente la estructura de tu historial.

## 1. El Merge (Fusión)
`git checkout main; git merge feature`
- **Técnicamente:** Git busca el antepasado común más cercano y crea un nuevo commit de unión que conecta las dos ramas.
- **Ventaja:** No es destructivo. El historial es exactamente lo que pasó cronológicamente.
- **Desventaja:** Genera muchos "Merge Commits" que ensucian el log visualmente.

## 2. El Rebase (Re-basar)
`git checkout feature; git rebase main`
- **Técnicamente:** Git "mueve" la base de tu rama actual al último commit de la rama destino. Aplica tus commits uno a uno sobre la nueva base.
- **Ventaja:** Crea un historial **lineal**. Parece que nunca te desviaste de `main`.
- **Desventaja:** **Reescribe la historia**. Los IDs (hashes) de tus commits cambian.

## 3. ¿Cuándo usar cada uno?
| Situación | Recomendación |
| :--- | :--- |
| Traer cambios de `main` a mi rama local | **Rebase** (Limpieza) |
| Integrar una `feature` completada en `main` | **Merge** (Visibilidad) |
| Rama compartida por varios desarrolladores | **NUNCA Rebase** (Romperás el Git ajeno) |

## 4. Peligros del Rebase
Si haces rebase de algo que ya está en el servidor (`push`), y otros compañeros han bajado ese código, cuando intentes hacer `push` de nuevo, Git te obligará a hacer un `force push`. Esto es una señal de peligro: alguien podría perder su trabajo.

## Resumen: Estética vs Veracidad
El Merge es honesto: te dice que hubo un desvío. El Rebase es estético: hace que el proyecto parezca una línea recta perfecta. Como Senior, usa rebase para limpiar tus ramas locales antes de que nadie las vea, y merge para integrar el resultado final.
