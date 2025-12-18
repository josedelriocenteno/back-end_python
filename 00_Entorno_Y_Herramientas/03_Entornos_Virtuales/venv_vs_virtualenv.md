# venv vs virtualenv

## 1. Introducción

En Python existen varias formas de crear entornos virtuales, siendo las más populares **`venv`** y **`virtualenv`**.  
Ambas cumplen la misma función de **aislar dependencias**, pero tienen diferencias que afectan su uso en proyectos profesionales.

> ⚠️ Nota:
> Conocer estas diferencias te permite elegir la herramienta más adecuada según el proyecto y la versión de Python.

---

## 2. venv

### 2.1 Descripción
- Incluido en Python desde la versión 3.3.  
- Permite crear un entorno virtual sin instalar paquetes adicionales.  
- Sencillo y suficiente para la mayoría de proyectos modernos.

### 2.2 Características
- Instalación rápida, integrada en Python.  
- No necesita permisos de administrador.  
- Soporta aislamiento completo de dependencias.  
- Limitaciones: menos opciones avanzadas comparado con `virtualenv`.

### 2.3 Ejemplo de uso

```bash
# Crear entorno virtual
python3.11 -m venv .venv

# Activar entorno
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install fastapi sqlalchemy
3. virtualenv
3.1 Descripción
Librería externa que funciona con Python 2 y 3.

Permite crear entornos virtuales incluso si venv no está disponible.

Muy usada en proyectos legacy o con versiones antiguas de Python.

3.2 Características
Compatible con versiones antiguas de Python.

Permite crear entornos con diferentes versiones de Python.

Opciones avanzadas como --system-site-packages.

Necesita instalación previa: pip install virtualenv.

3.3 Ejemplo de uso
bash
Copiar código
# Instalar virtualenv si no está
pip install virtualenv

# Crear entorno virtual
virtualenv .venv

# Activar entorno
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install fastapi sqlalchemy
4. Comparación venv vs virtualenv
Característica	venv	virtualenv
Inclusión en Python	Sí, desde 3.3	No, requiere instalación
Compatibilidad Python 2	No	Sí
Opciones avanzadas	Limitadas	Sí
Instalación de paquetes	pip incluido	pip incluido
Uso recomendado	Proyectos modernos	Proyectos legacy o flexibilidad extra

5. Buenas prácticas
Para proyectos nuevos, usar venv es suficiente.

Para proyectos antiguos o con necesidad de múltiples versiones de Python, usar virtualenv.

Crear siempre un entorno por proyecto.

Documentar en README cómo activar el entorno.

Ignorar el entorno en .gitignore para evitar subirlo al repositorio.

6. Ejemplo profesional
bash
Copiar código
# Proyecto moderno
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Proyecto legacy o con Python 2
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
7. Errores comunes a evitar
Usar Python global sin entorno virtual.

Mezclar entornos entre proyectos.

No documentar activación del entorno.

Subir el entorno al repositorio.

8. Checklist rápido
 Entorno virtual creado por proyecto

 Decidido entre venv (moderno) o virtualenv (legacy/flexibilidad)

 Dependencias instaladas y versionadas

 Documentación clara de activación

 .gitignore configurado para ignorar el entorno

9. Conclusión
venv y virtualenv cumplen la misma función de aislar dependencias, pero su elección depende de la versión de Python y necesidades del proyecto.
Para proyectos modernos, venv es suficiente y profesional.
Para proyectos legacy o con requisitos especiales, virtualenv ofrece mayor flexibilidad.