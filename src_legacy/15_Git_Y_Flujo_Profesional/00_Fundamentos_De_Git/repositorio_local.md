# El Repositorio Local: .git, HEAD y Staging Area

Para dominar Git, debes entender qué ocurre "bajo el capó" de tu carpeta de proyecto.

## 1. La Carpeta `.git`
Cuando haces `git init`, se crea esta carpeta oculta. Aquí reside TODA la magia. Si borras esta carpeta, dejas de tener un repositorio y pierdes todo el historial.

## 2. Los tres estados de Git
Un archivo en tu repositorio puede estar en uno de estos tres lugares:

### A. Directorio de Trabajo (Working Directory)
Los archivos tal y como los ves en tu editor. Son los cambios que estás haciendo pero que Git aún no ha "registrado".

### B. Área de Preparación (Staging Area / Index)
Un lugar intermedio. Aquí pones los cambios que quieres incluir en tu próximo commit.
- Comando: `git add <archivo>`

### C. Directorio de Git (Local Repo)
Donde Git guarda permanentemente las versiones del proyecto después de un commit.
- Comando: `git commit -m "..."`

## 3. ¿Qué es HEAD?
HEAD es un puntero especial que indica en qué punto del historial te encuentras actualmente. 
- Normalmente apunta al último commit de la rama en la que estás.
- Si "viajas al pasado" (`git checkout <hash>`), entraras en un estado de **Detached HEAD** (HEAD descolgado).

## 4. Integridad de Datos
Todo en Git se identifica por una cadena de 40 caracteres llamada **Hash SHA-1** (ej: `24b9a7...`). Es el DNI de cada commit, archivo y carpeta.

## Resumen: El flujo de datos
`Working Directory` --(add)--> `Staging Area` --(commit)--> `Git Directory`.
Entender el Staging Area es la clave para hacer commits limpios y organizados, permitiéndote elegir exactamente qué cambios subir y cuáles dejar para después.
