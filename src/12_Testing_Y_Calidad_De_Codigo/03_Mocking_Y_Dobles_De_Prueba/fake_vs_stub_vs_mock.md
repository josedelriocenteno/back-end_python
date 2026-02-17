# Dobles de Prueba: Fakes, Stubs y Mocks

En el testing profesional, solemos llamar a todo "un mock", pero técnicamente existen diferentes tipos de **Dobles de Prueba (Test Doubles)**. Conocer sus diferencias te ayudará a elegir la herramienta adecuada para cada situación.

## 1. DUMMY (Cuerpo presente)
Es un objeto que pasas solo porque la función lo requiere como argumento, pero nunca se usa realmente.
- **Uso:** Rellenar campos obligatorios de un constructor en un test que no prueba ese objeto.

## 2. STUB (Estado pre-programado)
Es un objeto que tiene respuestas fijas. No le importa cuántas veces lo llames ni con qué parámetros; siempre devuelve lo mismo.
- **Uso:** "Cuando pidas el precio de este producto, devuelve 10.0".
- **Enfoque:** Se centran en el **Estado**.

## 3. MOCK (Verificación de conducta)
A diferencia del Stub, el Mock se encarga de vigilar **cómo** se le llama.
- **Uso:** "¿Se llamó a la función de borrar el archivo?", "¿Se llamó con el ID correcto?".
- **Enfoque:** Se centran en el **Comportamiento / Interacción**.

## 4. FAKE (Implementación simplificada)
Es un objeto que tiene lógica real, pero simplificada para ser ultra rápida y no tener efectos secundarios.
- **Uso:** Una base de datos en memoria (SQLite) que sustituye a una base de datos pesada (PostgreSQL).
- **Ventaja:** Puedes usarlo casi como el objeto real, pero es mil veces más rápido.

## 5. SPY (El chismoso)
Es un objeto real que, además de funcionar, registra qué llamadas se le han hecho.
- **Diferencia:** El Mock sustituye al objeto; el Spy lo envuelve.

---

| Tipo | Propósito | ¿Tiene lógica? | ¿Verifica conducta? |
| :--- | :--- | :---: | :---: |
| **Dummy** | Rellenar | No | No |
| **Stub** | Surtir datos | Mínima | No |
| **Mock** | Verificar llamadas | No | **SÍ** |
| **Fake** | Sustituto rápido | **SÍ** | No |
| **Spy** | Registrar uso | **SÍ** | **SÍ** |

## Resumen: La caja de herramientas
- Usa **Stubs** para alimentar tus tests con datos.
- Usa **Mocks** para asegurar que se llamaron a las dependencias críticas (ej: enviar email).
- Usa **Fakes** para la base de datos de test.
- ¡No abuses! Si usas demasiados mocks, acabarás testeando "cómo está escrito el código" en lugar de "qué hace el código".
