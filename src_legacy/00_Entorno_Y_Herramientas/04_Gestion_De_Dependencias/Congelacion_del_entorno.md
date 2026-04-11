# Congelación del Entorno

## 1. Introducción

La **congelación del entorno** consiste en registrar todas las dependencias de un proyecto con sus versiones exactas.  
Esto asegura que **el proyecto se pueda reproducir de manera idéntica** en cualquier máquina o servidor.

> ⚠️ Nota:
> Sin congelar el entorno, otro desarrollador o el servidor de producción podría instalar versiones distintas, provocando errores inesperados.

---

## 2. Por qué es importante

1. **Reproducibilidad**
   - Garantiza que el proyecto funcione igual en todos los entornos.

2. **Estabilidad**
   - Evita errores por actualizaciones automáticas de librerías.

3. **Colaboración**
   - Todos los miembros del equipo usan exactamente las mismas dependencias.

4. **Producción segura**
   - Minimiza riesgos al desplegar en servidores o contenedores.

---

## 3. Herramientas para congelar el entorno

### 3.1 pip

```bash
# Congelar todas las dependencias con versiones exactas
pip freeze > requirements.txt

# Instalar dependencias congeladas en otro entorno
pip install -r requirements.txt
3.2 Poetry
bash
Copiar código
# Bloquear dependencias en poetry.lock
poetry install

# Instalar dependencias exactas en otro entorno
poetry install --no-root
💡 Tip:
Siempre versiona el archivo de congelación (requirements.txt o poetry.lock) en Git para mantener consistencia entre colaboradores y entornos de despliegue.

4. Diferencia entre congelar y versionar dependencias
Concepto	Descripción
Versionar	Definir rango de versiones compatibles (>=, <)
Congelar	Registrar versiones exactas (==)

⚠️ Recomendación profesional:
Para producción, siempre congelar dependencias con versiones exactas.
Para desarrollo, se pueden usar rangos flexibles, pero congelando para pruebas y despliegues.

5. Ejemplo práctico
bash
Copiar código
# Crear entorno virtual
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar librerías
pip install fastapi==0.100.0 sqlalchemy==2.0.20 uvicorn==0.24.0

# Congelar dependencias
pip freeze > requirements.txt

# Otro desarrollador recrea el entorno
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Resultado: idénticas versiones y comportamiento en todos los entornos.

6. Buenas prácticas
Congelar el entorno cada vez que se instalen o actualicen paquetes.

Versionar el archivo de congelación (requirements.txt o poetry.lock) en Git.

Mantener entornos separados por proyecto.

Revisar periódicamente el archivo congelado para actualizar parches de seguridad.

Documentar en README cómo recrear el entorno a partir del archivo congelado.

7. Errores críticos a evitar
No congelar el entorno antes de desplegar.

No versionar el archivo de congelación en el repositorio.

Mezclar paquetes con versiones flexibles y congeladas sin control.

Ignorar dependencias transitivas al congelar.

8. Checklist rápido
 Todas las dependencias congeladas con versiones exactas

 Archivo de congelación (requirements.txt o poetry.lock) versionado en Git

 Entorno virtual recreable en cualquier máquina

 Dependencias transitivas incluidas y controladas

 Documentación clara de cómo recrear el entorno

9. Conclusión
La congelación del entorno es una práctica esencial para cualquier proyecto Python profesional.
Garantiza reproducibilidad, estabilidad y seguridad.
No se trata solo de instalar paquetes: se trata de mantener un proyecto que funcione exactamente igual en todos los entornos y durante todo su ciclo de vida.