# Git Hooks: Tu primera línea de defensa

Los **Hooks** son scripts que Git ejecuta automáticamente en respuesta a ciertos eventos. Son la forma más efectiva de obligar (a ti mismo y a tu equipo) a mantener la calidad del código.

## 1. Tipos de Hooks
- **Pre-commit:** Se ejecuta antes de crear el commit. Ideal para pasar linters y tests rápidos.
- **Pre-push:** Antes de subir al remoto. Ideal para tests de integración pesados.
- **Commit-msg:** Para validar que el mensaje del commit sigue el estándar (ej: Conventional Commits).
- **Post-merge:** Tras un pull. Útil para reinstalar dependencias automáticamente.

## 2. Instalación de Hooks
Viven en `.git/hooks/`. Por defecto hay archivos de ejemplo `.sample`. Para activar uno, quítale la extensión y asegúrate de que sea ejecutable (`chmod +x`).

## 3. El framework `pre-commit`
Gestionar scripts de bash en `.git/hooks` es difícil de compartir con el equipo. Por eso usamos el paquete de Python `pre-commit`.
1. Instalas con `pip install pre-commit`.
2. Creas un archivo `.pre-commit-config.yaml`.
3. Ejecutas `pre-commit install`. Ahora el archivo vive en tu repo pero el script de Git apunta a él.

## 4. Hooks Recomendados
- **trailing-whitespace:** Borra espacios al final de las líneas.
- **end-of-file-fixer:** Asegura que los archivos terminan con una línea en blanco.
- **check-yaml / check-json:** Valida la sintaxis de archivos de configuración.
- **black / flake8 / isort:** Formateadores y linters de Python.

## 5. Saltar los Hooks
A veces tienes una emergencia y sabes que el código no pasa el linter pero quieres guardarlo.
`git commit -m "urgencia" --no-verify`
**⚠️ Úsalo solo en local y con moderación.**

## Resumen: Calidad por Defecto
Los Hooks quitan el "ruido" de las revisiones de código. Si el robot ya ha verificado los espacios y la sintaxis, el humano puede centrarse en lo importante: la lógica del negocio.
