# Debugger y Breakpoints en VSCode para Backend Python

## 1. Introducción

El **debugging profesional** es fundamental para detectar errores, entender flujos de ejecución y mantener código backend estable.  
VSCode proporciona un **depurador integrado** con soporte para breakpoints, inspección de variables y ejecución paso a paso.

> ⚠️ Nota:
> Depurar es una habilidad crítica. No depender solo de `print()` asegura eficiencia y profesionalismo.

---

## 2. Conceptos básicos

- **Breakpoint:** punto donde la ejecución se detiene para inspeccionar variables, stack y flujo.  
- **Step Over (F10):** ejecuta la línea actual y pasa a la siguiente sin entrar en funciones llamadas.  
- **Step Into (F11):** entra dentro de la función llamada para ver su ejecución interna.  
- **Step Out (Shift+F11):** sale de la función actual y vuelve al nivel superior.  
- **Watch:** permite observar variables específicas durante la ejecución.  
- **Call Stack:** muestra la pila de llamadas actual.

---

## 3. Configuración profesional de debugger

### 3.1 Archivo `launch.json`

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app.main:app", "--reload"],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
module: uvicorn permite depurar una aplicación FastAPI directamente.

justMyCode: true evita detenerse en librerías externas.

args: ["app.main:app", "--reload"] ejecuta la app con recarga automática.

4. Uso de breakpoints
4.1 Tipos de breakpoints
Breakpoint normal: se detiene siempre que se ejecuta esa línea.

Conditional breakpoint: se detiene solo si se cumple una condición específica.

python
Copiar código
# Ejemplo de condición
x = 10
y = 5
z = x + y  # breakpoint condicional: x > 5
Logpoint: imprime un mensaje en consola sin detener ejecución.

Function breakpoint: detiene ejecución al entrar en una función específica.

5. Inspección de variables y watch
Al detenerse en un breakpoint, VSCode permite:

Ver el valor de todas las variables locales.

Modificar valores en tiempo de ejecución.

Usar la ventana Watch para observar variables específicas.

python
Copiar código
user = {"name": "Juan", "email": "juan@example.com"}
# Puedes agregar user["email"] al Watch para monitorear cambios
6. Depuración profesional de proyectos backend
Configurar debugger para FastAPI, Celery u otras herramientas.

Evitar print() en producción; usar logging con niveles.

Combinar breakpoints con tests unitarios para aislar errores.

Usar remote debugging para depurar contenedores Docker o servidores remotos.

7. Buenas prácticas
Siempre depurar en entorno de desarrollo o staging, nunca producción.

Usar conditional breakpoints para no detener ejecución innecesariamente.

Documentar errores comunes encontrados y cómo reproducirlos con breakpoints.

Integrar debugging con linters y type checking para mayor seguridad.

8. Errores comunes a evitar
No configurar el intérprete Python correcto del entorno virtual.

Depurar en producción o con datos sensibles.

Ignorar el call stack y solo inspeccionar variables locales.

Usar print() en lugar de debugger profesional.

Depurar sin tests que aislen los errores, complicando reproducibilidad.

9. Checklist rápido
 Archivo launch.json configurado correctamente

 Breakpoints colocados estratégicamente (normales, condicionales, logpoints)

 Watch configurado para variables críticas

 Call stack y variables inspeccionadas durante la ejecución

 Depuración integrada con FastAPI, Docker o entornos remotos

 Uso de logging en lugar de prints para producción

10. Conclusión
El debugger y breakpoints en VSCode son herramientas profesionales imprescindibles para backend Python.
Dominar su uso permite diagnosticar problemas, entender flujos complejos y mantener la calidad y estabilidad del código.