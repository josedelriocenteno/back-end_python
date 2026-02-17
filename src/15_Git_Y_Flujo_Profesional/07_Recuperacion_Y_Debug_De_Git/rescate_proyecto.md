# Rescate de Proyecto: Cuando todo va mal

A veces, el repositorio entra en un estado incomprensible (conflictos sobre conflictos, borrados accidentales masivos, etc.). Aquí tienes el protocolo de emergencia.

## 1. El Botón del Pánico: Limpiar todo
Si quieres que tu carpeta local sea **exactamente** igual a lo que hay en el servidor ahora mismo, ignorando cualquier cosa que hayas hecho:
```bash
git fetch origin
git reset --hard origin/main
git clean -fd
```
- **Resultado:** Tu PC es un espejo de producción. Has perdido tus cambios locales, pero el proyecto vuelve a funcionar.

## 2. Buscar el commit que introdujo el bug (`git bisect`)
Si el proyecto funcionaba hace 2 semanas pero hoy no, y no sabes qué commit lo rompió:
1. `git bisect start`
2. `git bisect bad` (ahora no funciona)
3. `git bisect good <hash_de_hace_dos_semanas>`
4. Git irá saltando commits y tú solo tienes que probar la App y decir `git bisect good` o `git bisect bad`.
5. En pocos pasos, Git te señalará el commit exacto del culpable.

## 3. El error del "Archivo Gigante" en el historial
Si alguien subió por error un archivo de 1GB y lo borró en el siguiente commit, el archivo sigue ocupando espacio en la carpeta `.git`.
- **Solución:** Necesitas herramientas como **BFG Repo-Cleaner** o `git filter-branch` para reescribir la historia y borrar rastro de ese archivo para siempre.

## 4. Comprobar la integridad (`git fsck`)
Si sospechas que tu base de datos de Git local está corrupta (fallo de disco), este comando busca objetos huérfanos o corruptos.

## Resumen: Mantener la cabeza fría
Cualquier problema en Git tiene solución. Antes de borrar la carpeta del proyecto y clonar de nuevo, intenta entender qué ha pasado. Las herramientas de rescate te enseñarán más sobre Git que mil tutoriales de `add` y `commit`.
