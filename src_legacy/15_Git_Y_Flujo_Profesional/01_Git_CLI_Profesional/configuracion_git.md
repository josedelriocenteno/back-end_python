# Configuración Profesional: Tu firma en el código

Un entorno de Git mal configurado no solo te hace lento, sino que puede causar que tus commits aparezcan con el nombre de otro o que rompas archivos por culpa de los saltos de línea.

## 1. Identidad Global
Es lo primero que debes hacer en cualquier ordenador nuevo.
```bash
git config --global user.name "Tu Nombre Real"
git config --global user.email "tu@email.com"
```

## 2. Los Aliases: Ahorra años de vida
¿Por qué escribir `git status` si puedes escribir `git st`?
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm "commit -m"
```

## 3. Resolución de Saltos de Línea (CRLF vs LF)
Windows usa CRLF (`\r\n`) y Linux/Mac usa LF (`\n`). Si no lo controlas, Git verá cambios en todas las líneas de un archivo solo por los saltos de línea.
- **En Windows:** `git config --global core.autocrlf true`
- **En Mac/Linux:** `git config --global core.autocrlf input`

## 4. Gitignore Global
Para ignorar archivos basura de tu sistema (como `.DS_Store` o las carpetas de configuración de tu IDE `.vscode`) sin ensuciar el `.gitignore` del proyecto.
```bash
git config --global core.excludesfile ~/.gitignore_global
```

## 5. El Editor por Defecto
Asegúrate de que Git abra un editor que domines para los mensajes largos de commit o resolución de conflictos.
```bash
git config --global core.editor "code --wait" # Para VS Code
```

## Resumen: Hazlo Tuyo
Dedica 5 minutos a configurar tu `git config --global`. Un entorno personalizado es la marca de un profesional que cuida sus herramientas de trabajo.
