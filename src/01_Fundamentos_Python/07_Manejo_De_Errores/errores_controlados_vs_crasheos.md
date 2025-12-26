# Errores Controlados vs. Crasheos en Backend Python – Nivel Profesional

## 1. Concepto clave

- **Errores controlados:** situaciones esperadas que pueden ocurrir durante la ejecución normal (e.g., usuario ingresa datos inválidos, archivo no encontrado).  
  - Se capturan con `try/except`
  - Se manejan de manera que el sistema siga funcionando
  - Se loguean correctamente

- **Crasheos:** errores inesperados que no deberían ocurrir (e.g., fallo de librería externa, corrupción de datos interna).  
  - No se deben silenciar
  - El sistema puede detenerse de manera segura o alertar al equipo
  - Permite detectar problemas críticos temprano

---

## 2. Ejemplo de error controlado

```python
try:
    edad = int(input("Introduce tu edad: "))
except ValueError:
    print("Debe ingresar un número entero válido")
    edad = 0  # fallback seguro
Predecible

Mantiene el flujo

Informativo

3. Ejemplo de crasheo intencional
python
Copiar código
def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b

# Si alguien intenta dividir entre cero, fallará
resultado = dividir(10, 0)
Este error no se atrapa aquí, porque es crítico

Se espera que el sistema maneje/loguee el crash

Evita ocultar bugs graves

4. Buenas prácticas profesionales
Atrapa solo lo que esperas: nunca uses except Exception genérico sin necesidad.

Loguea siempre: incluso errores controlados deben ser registrados.

Fallback seguro: si manejas el error, asegúrate de que el sistema siga estable.

Crasheos claros: si algo inesperado sucede, deja que falle para detectar y corregir el problema.

Jerarquía de excepciones: usar tus propias excepciones ayuda a diferenciar errores controlados de crasheos.

5. Patrón profesional
python
Copiar código
try:
    procesar_datos(datos)
except ErrorValidacion as e:
    logging.warning(f"Error controlado: {e}")
except ErrorConexionBD as e:
    logging.error(f"Error crítico: {e}")
    raise  # crash intencional para alertar al equipo
ErrorValidacion → controlado, flujo continúa

ErrorConexionBD → crítico, crash intencional, alerta activa

6. Errores comunes de juniors
Silenciar errores críticos con pass

Atrapar todo con except Exception → errores graves ocultos

No usar logging → debugging imposible

Mezclar controlados con crasheos → código confuso y peligroso

7. Checklist mental backend
✔️ Este error es predecible o crítico?

✔️ Lo manejo o dejo que falle?

✔️ Logging configurado correctamente?

✔️ Fallback seguro si lo manejo?

✔️ Crasheo intencional genera alerta clara?

8. Regla de oro
Atrapa errores esperados y manejables, deja que los errores graves crasheen de manera controlada.
Esto mantiene tu backend estable, confiable y profesional.

yaml
Copiar código

---

🔥 **Verdad profesional**  
Saber distinguir **controlados vs crasheos** es lo que evita que tu backend se vuelva **un caos silencioso**.  
