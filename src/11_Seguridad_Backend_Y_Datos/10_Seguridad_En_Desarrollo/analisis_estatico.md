# Análisis Estático de Seguridad (SAST)

El SAST (Static Application Security Testing) consiste en analizar el código fuente **sin ejecutarlo** en busca de patrones inseguros. Es como pasar un corrector ortográfico pero de seguridad.

## 1. Por qué es útil
Detecta errores humanos antes de que lleguen siquiera al Code Review:
- Inyecciones SQL obvias.
- Uso de funciones inseguras (ej: `pickle`, `yaml.load` sin seguridad).
- Contraseñas o claves de API hardcodeadas.
- Configuraciones de servidor de desarrollo que se han quedado en producción.

## 2. Herramientas Líderes para Python
- **Bandit:** La herramienta especializada en seguridad para Python por excelencia. Busca fallos comunes y los clasifica por gravedad.
- **Flake8-security:** Un plugin para el linter normal que añade reglas de seguridad.
- **SonarQube:** Una plataforma completa que mide calidad y seguridad del código a largo plazo.

## 3. Ejemplo de lo que detecta Bandit:
```python
# Bandit lanzará una alerta 'High Severity' aquí
import os
os.system("rm -rf " + user_input) # Vulnerable a Command Injection
```

## 4. Integración en el IDE
Lo ideal es ver los fallos mientras escribes. Instala plugins de Bandit o SonarLint en VS Code / PyCharm. Arreglar un fallo en el segundo 1 es 100 veces más barato que arreglarlo tras haber sido desplegado.

## 5. Falsos Positivos en SAST
A veces Bandit se queja de un `os.chmod` que es legítimo. No borres la regla global; usa comentarios específicos para ignorar esa línea:
`# nosec` (Bandit) o `# noqa` (Flake8). Pero hazlo con moderación y documentando el porqué.

## Resumen: El linter de seguridad
El análisis estático es la primera línea de defensa en la pipeline de desarrollo. Es rápido, barato y evita que los errores más "tontos" (pero peligrosos) de seguridad lleguen a ojos de otros desarrolladores o atacantes.
