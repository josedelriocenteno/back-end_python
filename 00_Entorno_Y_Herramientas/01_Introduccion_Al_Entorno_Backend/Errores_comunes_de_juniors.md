# Errores Comunes de Juniors

## 1. Introducción

Cuando comienzas en desarrollo backend, hay errores que casi todos los juniors cometen.  
Algunos son pequeños y fáciles de corregir, otros pueden generar **deuda técnica o fallos críticos en producción**.  
Conocerlos de antemano y cómo evitarlos es clave para crecer rápido y profesionalmente.

> ⚠️ Nota:
> Cometer errores es normal, pero **repetir los mismos errores una y otra vez es lo que diferencia a un junior de un profesional**.

---

## 2. Errores Más Frecuentes

### 2.1 Uso del Python Global
- Instalar paquetes directamente en la instalación global de Python.  
- Problema: puede romper otros proyectos o crear conflictos de versiones.
- Solución: **siempre usar entornos virtuales aislados** (`venv`, `poetry`).

### 2.2 No Gestionar Dependencias
- Instalar librerías sin control de versiones ni registro (`requirements.txt` o `poetry.lock`).  
- Problema: reproducibilidad cero, difícil colaborar o desplegar.  
- Solución: **congelar dependencias y usar archivos de lock**.

### 2.3 Código Monolítico y Sin Modularidad
- Todo el código en un solo archivo o clase gigante.  
- Problema: difícil de mantener, testear o escalar.  
- Solución: **separar por capas, módulos y responsabilidades claras**.

### 2.4 Hardcodear Configuraciones
- Poner credenciales, rutas o URLs directamente en el código.  
- Problema: inseguro y no escalable.  
- Solución: **usar variables de entorno y archivos `.env`**.

### 2.5 No Usar Control de Versiones Correctamente
- Commits desordenados, sin mensajes claros o sin ramas.  
- Problema: difícil revertir cambios, colaborar o hacer seguimiento.  
- Solución: **adoptar un flujo profesional de Git (`feature/`, `develop`, `main`) y commits semánticos**.

### 2.6 Ignorar Testing
- No escribir tests o hacer pruebas manuales poco fiables.  
- Problema: errores silenciosos y código frágil.  
- Solución: **pytest, tests unitarios e integraciones automáticas**.

### 2.7 Falta de Documentación
- Código sin comentarios ni README explicativo.  
- Problema: otros desarrolladores no entienden tu trabajo, onboarding lento.  
- Solución: **documentar módulos, funciones y setup del proyecto**.

### 2.8 No Usar Linters y Formatters
- Código con estilos inconsistentes y errores de sintaxis sutiles.  
- Problema: difícil lectura y mantenimiento.  
- Solución: **Black, Flake8, Mypy y pre-commit hooks**.

### 2.9 Ignorar la Reproducibilidad del Entorno
- No considerar que otro desarrollador o servidor de producción pueda tener un entorno distinto.  
- Problema: errores difíciles de replicar.  
- Solución: **entorno reproducible con `requirements.txt` / `poetry.lock` y Docker si es necesario**.

### 2.10 No Revisar Código Antes de Merge
- Merge directo a main sin revisión.  
- Problema: bugs en producción, código inconsistente.  
- Solución: **pull requests y code review obligatorio**.

---

## 3. Ejemplo práctico de errores comunes

```bash
# ERROR: usando Python global
pip install fastapi sqlalchemy
python main.py  # Funciona en tu máquina pero rompe en otra

# ERROR: hardcodeando configuración
DATABASE_URL = "postgres://usuario:password@localhost:5432/db"

# ERROR: código monolítico
def main():
    # cientos de líneas sin modularidad
    ...
Cómo debería hacerse profesionalmente:

bash
Copiar código
# Crear entorno virtual
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar dependencias con versiones controladas
pip install fastapi==0.100.0 sqlalchemy==2.0.20
pip freeze > requirements.txt

# Configuración separada
# .env
DATABASE_URL=postgres://usuario:password@localhost:5432/db
4. Checklist de Prevención
 Entorno virtual activo

 Dependencias gestionadas y reproducibles

 Código modular y limpio

 Configuración separada del código

 Git correctamente usado con commits claros

 Tests automatizados implementados

 Documentación mínima del proyecto

 Linters y formatters configurados

 Reproducibilidad garantizada

 Revisiones de código antes de merge

5. Conclusión
Evitar estos errores desde el principio acelera tu curva de aprendizaje y te acerca a un nivel profesional real.
La clave está en mentalidad profesional, buenas prácticas y disciplina desde el día 1.
No es suficiente que el código funcione; debe ser seguro, mantenible, reproducible y colaborativo.