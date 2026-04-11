# Gitignore Profesional: Higiene en el Repositorio

Un `.gitignore` no es solo una lista de archivos que no quieres ver; es un documento que define la portabilidad y limpieza de tu proyecto.

## 1. La Filosofía del Gitignore
"Solo versiona lo que un desarrollador necesita para CONSTRUIR el proyecto, no el resultado de la construcción ni las herramientas personales".

## 2. Qué ignorar (Categorías)
- **Dependencias:** `.venv/`, `node_modules/`, `build/`.
- **Archivos de Sistema:** `.DS_Store`, `Thumbs.db`.
- **Configuración de IDE:** `.vscode/`, `.idea/`.
- **Datos y Logs:** `*.log`, `data/*.csv` (si son gigantes), `__pycache__/`.
- **Secretos:** `.env`, `*.key`.

## 3. Estructura de un archivo `.gitignore` profesional
Usa comentarios para organizar:
```text
# --- ENTORNO ---
.venv/
ENV/

# --- LENGUAJE (Python) ---
__pycache__/
*.py[cod]

# --- IDEs ---
.vscode/
.idea/

# --- DATOS ---
/data/raw/
!/data/sample.csv  # Excepción: queremos este ejemplo
```

## 4. El truco del "Not" (`!`)
A veces quieres ignorar una carpeta entera pero mantener un archivo específico dentro.
```text
/config/*
!/config/template.json
```

## 5. Forzar el seguimiento (`-f`)
Si necesitas subir un archivo que está en el gitignore por una excepción temporal:
`git add -f archivo_ignorado.py`

## Resumen: Repositorios esbeltos
Un `.gitignore` bien hecho evita "ruido" en las Pull Requests y asegura que el repositorio ocupe solo el espacio estrictamente necesario. Usa plantillas de [gitignore.io](https://www.toptal.com/developers/gitignore) para tu lenguaje específico.
