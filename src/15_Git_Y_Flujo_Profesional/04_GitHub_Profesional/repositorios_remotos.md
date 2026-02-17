# Repositorios Remotos: Origin, Upstream y el mundo exterior

Un repositorio no es una isla. Para que sea útil, debe estar conectado a la nube y a otros desarrolladores.

## 1. ¿Qué es un Remote?
Es simplemente una URL que apunta a una copia de tu repositorio en otro servidor (GitHub).
- Comprobar remotos: `git remote -v`

## 2. Origin: Tu centro de mando
Por defecto, cuando clonas un repositorio, Git llama `origin` a la URL de donde lo has bajado. Es tu referencia principal para hacer `push` y `pull`.

## 3. Upstream: El origen de la verdad
En proyectos Open Source o cuando haces un **Fork**, necesitas una segunda referencia.
- **Upstream** suele ser la URL del proyecto original del que tú te has hecho una copia.
- Lo usas para traer las actualizaciones del proyecto original a tu fork.
```bash
git remote add upstream https://github.com/original/repo.git
git fetch upstream
git merge upstream/main
```

## 4. Gestión de múltiples remotos
Puedes tener tantos como quieras. Útil si despliegas a Heroku (`git push heroku main`) o si trabajas con varios proveedores a la vez.

## 5. Cambiar URLs
Si el proyecto se mueve de organización o cambia de nombre:
`git remote set-url origin https://github.com/nueva/url.git`

## Resumen: Desacoplamiento
Los remotos te permiten sincronizar tu trabajo con el resto del mundo. Entender la diferencia entre `origin` (tu copia) y `upstream` (el original) es clave para contribuir a proyectos de gran escala.
