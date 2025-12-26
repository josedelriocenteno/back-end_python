# Buenas Prácticas con Entornos Virtuales

## 1. Introducción

Usar un entorno virtual correctamente es crucial en proyectos Python profesionales.  
No basta con crearlo; **hay buenas prácticas que garantizan estabilidad, reproducibilidad y seguridad**.

> ⚠️ Nota:
> Ignorar estas prácticas puede generar conflictos de dependencias, errores difíciles de reproducir y problemas de seguridad en producción.

---

## 2. Crear un entorno por proyecto

- Cada proyecto debe tener su propio entorno virtual (`venv` o `virtualenv`).  
- Evita conflictos de librerías entre proyectos.  
- Mantiene limpio el Python del sistema.

```bash
# Ejemplo
python3.11 -m venv .venv
source .venv/bin/activate
3. Activación y desactivación correcta
Siempre activar el entorno antes de instalar paquetes o ejecutar scripts.

Desactivar al finalizar para no interferir con otros proyectos.

bash
Copiar código
# Activar
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Desactivar
deactivate
4. Versionado y gestión de dependencias
Congelar dependencias para asegurar reproducibilidad: pip freeze > requirements.txt.

Usar herramientas como Poetry para control de versiones y entornos automáticos.

Evitar instalar paquetes globales dentro del entorno virtual.

bash
Copiar código
# Congelar dependencias
pip freeze > requirements.txt

# Instalar a partir de archivo
pip install -r requirements.txt
5. Ignorar el entorno en el repositorio
Añadir .venv/ a .gitignore para no subir archivos del entorno virtual.

Evita sobrecargar el repositorio y conflictos en otros equipos.

markdown
Copiar código
# .gitignore
.venv/
__pycache__/
*.pyc
6. Mantener entornos limpios y actualizados
Revisar y eliminar dependencias no usadas.

Actualizar paquetes de forma controlada y probar compatibilidad.

Re-crear el entorno cuando haya conflictos críticos o versiones corruptas.

bash
Copiar código
# Re-crear entorno
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
7. Documentación clara
Indicar en README cómo activar y recrear el entorno.

Registrar versión de Python y dependencias principales.

Facilita onboarding de nuevos desarrolladores y reproducibilidad.

bash
Copiar código
# README.md ejemplo
# Activación del entorno
python3.11 -m venv .venv
source .venv/bin/activate

# Instalación de dependencias
pip install -r requirements.txt
8. Evitar errores comunes
No usar entornos virtuales y depender del Python global.

Mezclar entornos entre proyectos.

Instalar paquetes sin versionado fijo.

Subir el entorno al repositorio.

9. Checklist rápido
 Entorno virtual por proyecto

 Activación y desactivación correcta

 Dependencias congeladas y versionadas

 .gitignore configurado

 Documentación de activación clara

 Entorno limpio y actualizado regularmente

10. Conclusión
Seguir buenas prácticas con entornos virtuales garantiza que tu proyecto sea estable, reproducible y profesional.
No basta con crear el entorno; debes mantenerlo, documentarlo y usarlo correctamente desde el día 1.