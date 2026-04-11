# pip y requirements.txt

## 1. Introducción

En Python, **pip** es la herramienta estándar para instalar y gestionar librerías.  
`requirements.txt` es un archivo que documenta las dependencias del proyecto, incluyendo sus versiones exactas.  
Usarlos correctamente es **clave para la reproducibilidad y estabilidad de proyectos profesionales**.

> ⚠️ Nota:
> Instalar paquetes sin versionado o sin registrar en `requirements.txt` es un error crítico que puede romper tu proyecto en otra máquina o en producción.

---

## 2. pip: Gestión de paquetes

### 2.1 Comandos esenciales

```bash
# Instalar un paquete
pip install fastapi

# Instalar versión específica
pip install fastapi==0.100.0

# Actualizar paquete
pip install --upgrade fastapi

# Desinstalar paquete
pip uninstall fastapi
2.2 Buenas prácticas con pip
Siempre activar el entorno virtual antes de instalar paquetes.

Instalar versiones fijas para garantizar reproducibilidad.

Evitar instalar paquetes globalmente.

Revisar compatibilidad con otras librerías antes de instalar.

3. requirements.txt
3.1 Qué es
Archivo que lista todas las dependencias del proyecto con versiones exactas.

Permite reproducir el entorno en otra máquina o servidor.

Convención estándar en proyectos Python profesionales.

3.2 Crear y usar
bash
Copiar código
# Congelar dependencias del entorno actual
pip freeze > requirements.txt

# Instalar dependencias en otro entorno
pip install -r requirements.txt
3.3 Ejemplo de requirements.txt
ini
Copiar código
fastapi==0.100.0
sqlalchemy==2.0.20
uvicorn==0.24.0
pydantic==2.5.1
💡 Tip:
Incluir siempre versiones exactas para evitar que actualizaciones de librerías rompan tu proyecto.

4. Versiones flexibles vs fijas
Tipo de versión	Sintaxis	Pros	Contras
Fija	fastapi==0.100.0	Reproducible, seguro	No se actualiza automáticamente
Flexibles	fastapi>=0.100.0,<0.101	Permite parches y mejoras	Riesgo de romper compatibilidad

⚠️ Recomendación profesional:
Para producción, usar versiones fijas.
Para desarrollo experimental, se pueden usar versiones flexibles con cuidado.

5. Ejemplo práctico
bash
Copiar código
# Proyecto nuevo
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar paquetes y congelar dependencias
pip install fastapi==0.100.0 sqlalchemy==2.0.20 uvicorn==0.24.0
pip freeze > requirements.txt

# Otro desarrollador clona el proyecto
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py  # Funciona exactamente igual
6. Buenas prácticas profesionales
Congelar siempre las dependencias en requirements.txt.

Revisar y actualizar paquetes periódicamente, probando compatibilidad.

Evitar instalar paquetes globalmente o sin versionado.

Documentar en README cómo instalar dependencias con pip.

Integrar instalación de dependencias en scripts de CI/CD para reproducibilidad automática.

7. Errores críticos a evitar
Instalar paquetes sin entorno virtual.

No versionar dependencias.

Subir dependencias globales al repositorio.

No actualizar requirements.txt después de instalar o actualizar paquetes.

8. Checklist rápido
 Entorno virtual activo

 Dependencias instaladas con pip dentro del entorno

 requirements.txt actualizado y versionado

 Documentación clara de instalación en README

 Versiones fijas usadas para producción

9. Conclusión
Usar pip junto a requirements.txt correctamente garantiza que tu proyecto sea reproducible, seguro y profesional.
No basta con que funcione en tu máquina; debe ejecutarse igual en cualquier entorno de desarrollo o producción.