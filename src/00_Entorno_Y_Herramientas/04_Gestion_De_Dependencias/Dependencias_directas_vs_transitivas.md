# Dependencias Directas vs Transitivas

## 1. Introducción

En cualquier proyecto Python, entender la diferencia entre **dependencias directas y transitivas** es clave para mantener un entorno limpio, reproducible y estable.

- **Dependencias directas:** librerías que tu proyecto importa y utiliza explícitamente.  
- **Dependencias transitivas:** librerías que son requeridas por tus dependencias directas, pero que tú no usas directamente.

> ⚠️ Nota:
> Ignorar las dependencias transitivas puede generar conflictos de versiones y errores difíciles de depurar.

---

## 2. Dependencias directas

### 2.1 Definición
Son las librerías que **tú decides instalar y usar directamente en tu código**.

### 2.2 Ejemplo

```bash
# Instalo FastAPI para mi proyecto
pip install fastapi==0.100.0
FastAPI es una dependencia directa porque tu código la importa y la usa.

python
Copiar código
from fastapi import FastAPI

app = FastAPI()
3. Dependencias transitivas
3.1 Definición
Son las librerías que no importas directamente, pero que tu dependencia directa necesita para funcionar.

3.2 Ejemplo
FastAPI requiere pydantic y starlette para funcionar.

Estas librerías son dependencias transitivas.

bash
Copiar código
pip install fastapi==0.100.0
pip freeze
# Salida:
# fastapi==0.100.0
# pydantic==2.5.1   # transitiva
# starlette==0.28.1  # transitiva
💡 Tip:
Aunque no uses directamente una dependencia transitiva, debes controlar su versión para evitar incompatibilidades.

4. Problemas comunes con dependencias transitivas
Conflictos de versión

Dos librerías requieren versiones diferentes de la misma dependencia transitiva.

Puede romper tu proyecto en producción.

Actualizaciones inesperadas

Actualizar una dependencia directa puede actualizar transitivas sin que lo notes.

Incompatibilidad entre entornos

Otro desarrollador o servidor de producción puede tener versiones distintas de transitivas si no se congela el entorno.

5. Cómo gestionarlas profesionalmente
5.1 Congelar todas las dependencias
bash
Copiar código
pip freeze > requirements.txt
Esto asegura que directas y transitivas queden registradas con versión exacta.

5.2 Revisar dependencias transitivas
Herramientas como pipdeptree permiten visualizar árbol de dependencias:

bash
Copiar código
pip install pipdeptree
pipdeptree
Salida ejemplo:

yaml
Copiar código
fastapi==0.100.0
  - pydantic [required: >=2.5.0, installed: 2.5.1]
  - starlette [required: >=0.28.0, installed: 0.28.1]
Permite identificar conflictos antes de que afecten al proyecto.

5.3 Usar herramientas modernas
Poetry: gestiona dependencias directas y transitivas automáticamente, bloqueando versiones en poetry.lock.

pip-tools: permite generar un requirements.txt reproducible con dependencias transitivas controladas.

6. Ejemplo profesional
bash
Copiar código
# Crear entorno virtual
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar dependencia directa
pip install fastapi==0.100.0

# Revisar árbol de dependencias
pipdeptree

# Congelar todas las dependencias (directas y transitivas)
pip freeze > requirements.txt
7. Buenas prácticas
Controlar todas las dependencias con versiones exactas.

Revisar el árbol de dependencias transitivas antes de actualizar paquetes.

Usar herramientas que bloqueen versiones (pip freeze, Poetry).

Evitar instalar paquetes globalmente que puedan entrar en conflicto.

Documentar en README cómo recrear el entorno con todas las dependencias.

8. Checklist rápido
 Dependencias directas identificadas

 Dependencias transitivas controladas y versionadas

 Reproducibilidad garantizada con requirements.txt o poetry.lock

 Árbol de dependencias revisado antes de actualizar paquetes

 Entorno virtual activo y documentado

9. Conclusión
Gestionar correctamente dependencias directas y transitivas es esencial para proyectos Python profesionales.
Un proyecto reproducible y estable depende tanto de las librerías que usas directamente como de las que estas requieren.
Ignorar esto puede generar conflictos, errores silenciosos y problemas graves en producción.