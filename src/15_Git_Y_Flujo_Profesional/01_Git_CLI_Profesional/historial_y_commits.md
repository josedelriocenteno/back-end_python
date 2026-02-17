# Historial y Commits: Viajando por la línea del tiempo

El historial de Git no es solo una lista; es la memoria viva del proyecto. Saber leerlo es fundamental para encontrar el origen de un bug.

## 1. El Hash: El ADN del commit
Cada commit tiene un identificador único (SHA-1) de 40 caracteres.
- **Dato:** Normalmente con los primeros 7 caracteres (`7a2b3c4`) es suficiente para identificarlo.

## 2. Navegación por el log
- `git log --graph`: Dibuja el árbol de ramas en la terminal.
- `git log --author="Nombre"`: Filtra commits de una persona específica.
- `git log --grep="bug"`: Busca palabras clave en los mensajes de commit.

## 3. ¿Quién cambió esta línea? (`git blame`)
A pesar de su nombre negativo ("echar la culpa"), es la mejor herramienta para entender el contexto.
- `git blame archivo.py`: Muestra para cada línea quién fue el último en modificarla y en qué commit.
- **Tip VS Code:** Instala la extensión **GitLens** para ver el "blame" de forma elegante sobre cada línea.

## 4. Viaje en el tiempo (Checkout)
Si quieres ver cómo era el proyecto hace 3 días:
- `git checkout <hash>`
- **⚠️ Nota:** Estarás en estado "Detached HEAD". No hagas cambios aquí; solo mira y vuelve con `git switch -`.

## 5. El poder de `git reflog`
Es el "historial del historial". Registra cada vez que el HEAD se mueve, incluso si borras una rama o haces un reset.
- Si parece que has "borrado" algo por error en Git, el `reflog` suele ser el salvavidas.

## Resumen: El proyecto tiene memoria
No ignores el historial. Un buen desarrollador sabe consultar el pasado para tomar mejores decisiones en el presente.
