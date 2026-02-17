# Aislar Dependencias: La Clave del Determinismo

Un test **determinista** es aquel que siempre devuelve el mismo resultado ante el mismo código. Si tus tests dependen de factores externos, dejan de ser deterministas y se vuelven inestables.

## 1. El Enemigo: La "Impureza"
Un test es "impuro" si depende de:
- **La Hora del Sistema:** `datetime.now()` cambia cada microsegundo.
- **La Red:** Una caída de internet o lentitud en una API externa (Stripe, Google).
- **El Orden de Ejecución:** El Test B solo pasa si el Test A borró la DB antes.
- **Variables Globales Mutables.**

## 2. Cómo Aislar: Estrategias Senior

### A. Inyección de Dependencias
No instancies clases pesadas dentro de tus funciones. Pásalas como argumento.
- En producción pasas la clase real.
- En los tests pasas un **Mock** o un **Stub**.

### B. Mocks de Tiempo
Usa librerías como `freezegun` para "congelar" el tiempo en un momento exacto.
```python
from freezegun import freeze_time

@freeze_time("2024-01-01 12:00:00")
def test_calculo_vencimiento():
    # Siempre pensará que hoy es 1 de enero de 2024
    assert calcular_fecha() == "2024-01-31"
```

### C. VCR.py (Grabación de Red)
Si tienes que testear una integración con una API real, `vcr.py` graba la primera respuesta HTTP en un archivo `.yaml` (Cassette). Las siguientes veces, Pytest leerá el archivo en lugar de hacer la llamada real.
- **Resultado:** Tests ultra rápidos y que funcionan sin internet.

## 3. Fixtures de Limpieza (Sandboxing)
Asegúrate de que cada test corre en un "Cajón de Arena" (Sandbox).
- Si creas un archivo de test, bórralo en el Teardown.
- Si insertas en la DB, usa una transacción que haga `rollback` al terminar el test.

## Resumen: Fiabilidad Total
Tu objetivo como desarrollador senior es que cuando la pipeline de CI se ponga en rojo, todo el equipo diga: "Hay un bug". Si dicen "A saber qué ha pasado esta vez, dale a reintentar", es que has fallado aislando tus dependencias.
