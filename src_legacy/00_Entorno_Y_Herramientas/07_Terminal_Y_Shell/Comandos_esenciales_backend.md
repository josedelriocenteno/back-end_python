# Comandos Esenciales para Backend Python en la Terminal

## 1. Introducción

Dominar los **comandos esenciales de la terminal** es clave para cualquier desarrollador backend.  
Permite ejecutar scripts, gestionar entornos, controlar versiones, trabajar con bases de datos y automatizar tareas de forma profesional.

> ⚠️ Nota:
> No se trata solo de saber escribir comandos, sino de **entender qué hacen y cómo integrarlos en flujos de trabajo eficientes**.

---

## 2. Gestión de directorios y archivos

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `ls -la` | Listar todos los archivos y carpetas incluyendo ocultos | `ls -la` |
| `cd <directorio>` | Cambiar de directorio | `cd ~/proyecto_backend` |
| `pwd` | Mostrar ruta actual | `pwd` |
| `mkdir <nombre>` | Crear directorio | `mkdir logs` |
| `rm -rf <directorio>` | Eliminar directorio y contenido | `rm -rf old_backup` |
| `touch <archivo>` | Crear archivo vacío | `touch main.py` |
| `cat <archivo>` | Ver contenido de archivo | `cat README.md` |

---

## 3. Gestión de Python y entornos virtuales

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows PowerShell

# Instalar dependencias
pip install -r requirements.txt

# Congelar dependencias
pip freeze > requirements.txt

# Ejecutar script Python
python main.py
💡 Tip:
Mantener entornos virtuales separados por proyecto garantiza reproducibilidad y evita conflictos de dependencias.

4. Gestión de Git
Comando	Descripción	Ejemplo
git status	Ver estado de cambios	git status
git add <archivo>	Añadir archivo al staging	git add app/main.py
git commit -m "mensaje"	Hacer commit con mensaje	git commit -m "Agregar endpoint de usuarios"
git push	Subir cambios al repositorio remoto	git push origin main
git pull	Traer cambios del remoto	git pull origin main
git branch	Listar ramas	git branch
git checkout <rama>	Cambiar de rama	git checkout feature/login

⚠️ Nota:
Integrar estos comandos con VSCode Git y GitLens mejora la productividad y reduce errores.

5. Gestión de bases de datos (PostgreSQL ejemplo)
bash
Copiar código
# Conectar a base de datos
psql -h localhost -U usuario -d mydb

# Ejecutar script SQL
psql -h localhost -U usuario -d mydb -f scripts/init.sql

# Exportar base de datos
pg_dump -U usuario mydb > backup.sql

# Importar base de datos
psql -U usuario -d mydb < backup.sql
💡 Tip:
Conocer comandos de DB en terminal permite integrarlos en scripts de CI/CD y despliegue.

6. Gestión de Docker (opcional pero profesional)
bash
Copiar código
# Construir imagen
docker build -t mi_app .

# Ejecutar contenedor
docker run -d -p 8000:8000 mi_app

# Listar contenedores
docker ps

# Detener contenedor
docker stop <container_id>

# Levantar servicios definidos en docker-compose
docker-compose up -d

# Detener servicios docker-compose
docker-compose down
7. Automatización y flujos de trabajo
Combinar comandos en una sola línea:

bash
Copiar código
source .venv/bin/activate && pytest tests/ && flake8 app/
Ejecutar scripts de mantenimiento:

bash
Copiar código
# Limpiar logs antiguos y reiniciar servidor
rm -rf logs/*.log && uvicorn app.main:app --reload
Usar alias en .bashrc o .zshrc para comandos frecuentes:

bash
Copiar código
alias runserver="source .venv/bin/activate && uvicorn app.main:app --reload"
alias testall="pytest tests/ --maxfail=3 --disable-warnings"
8. Buenas prácticas profesionales
Aprender los comandos básicos y combinarlos en scripts para automatizar tareas.

Siempre trabajar dentro del entorno virtual para evitar conflictos de dependencias.

Usar alias y scripts para tareas repetitivas.

Integrar Git y Docker en la terminal para flujo de trabajo profesional.

Evitar ejecutar comandos peligrosos sin revisar (rm -rf, docker system prune).

9. Errores comunes a evitar
Ejecutar scripts Python sin activar el entorno virtual.

Mezclar comandos locales con producción sin cuidado.

No versionar cambios con Git antes de ejecutar scripts críticos.

Olvidar verificar contenedores Docker activos antes de iniciar nuevos.

Copiar comandos sin adaptarlos a rutas y entornos del proyecto.

10. Checklist rápido
 Comandos básicos de directorios y archivos dominados

 Entorno virtual creado y activado correctamente

 Comandos Git esenciales dominados e integrados con VSCode

 Conexión y operaciones básicas con bases de datos desde terminal

 Comandos Docker básicos dominados

 Scripts y alias configurados para automatización

 Flujo profesional reproducible y seguro

11. Conclusión
Dominar los comandos esenciales en la terminal permite trabajar de manera eficiente, profesional y reproducible en proyectos backend Python.
Integrar estos comandos en scripts y flujos de trabajo asegura calidad, velocidad y seguridad en el desarrollo.