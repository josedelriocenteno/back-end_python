# Errores Comunes y Cómo NO romper el repositorio

Git es muy permisivo, pero hay ciertos errores de "Novato" que pueden causar horas de trabajo a todo el equipo para arreglarlos.

## 1. Hacer Rebase de Ramas Compartidas
Si haces rebase de `develop` o `main`, cambias la base para todos. Obligarás a tus compañeros a hacer cosas complejas para resincronizar. **NUNCA hagas rebase de una rama que no sea puramente tuya (local).**

## 2. Force Push (`git push -f`)
Es como una granada. Dice: "Ignora lo que haya en el servidor y pon lo mío".
- Solo úsalo en ramas de feature personales tras un rebase.
- Nunca lo uses en `main`.

## 3. Subir el Directorio `.venv` o `node_modules`
Saturar el repositorio con miles de archivos de librerías externas que no necesitamos versionar.
- **Solución:** `gitignore` bien configurado desde el minuto 1.

## 4. Commits Gigantes
Mezclar cambios de UI, base de datos y lógica de negocio. Si el cambio de base de datos rompe algo, no puedes revertirlo sin perder el trabajo de la UI.
- **Solución:** Commits pequeños y atómicos.

## 5. Trabajar siempre en `main`
Es el error número uno. Si rompes `main`, rompes el trabajo de todo el equipo y bloqueas los despliegues.
- **Solución:** Ramas siempre.

## 6. Ignorar los mensajes de error
Muchos desarrolladores ven un error de Git y prueban comandos al azar de StackOverflow (`--force`, `--hard`). 
- **Solución:** Lee el error. Git suele decirte exactamente qué hacer para arreglarlo.

## Resumen: Responsabilidad Compartida
El repositorio es la casa de todos los desarrolladores del proyecto. Mantenerlo limpio y seguir las normas de seguridad e integración es el primer paso para ser un compañero de equipo valioso.
