# Mitigaciones Prácticas: Tu Escudo de Desarrollo

Más allá de conocer los ataques, como desarrollador backend debes tener un "set de herramientas" de mitigación listas para aplicar en cada sprint.

## 1. Validación de Entrada Estricta (Input Sanitization)
No solo compruebes el tipo de dato, comprueba el contenido.
- **Mal:** `age: int`
- **Bien:** `age: Annotated[int, Field(gt=0, lt=120)]`. Un usuario no puede tener -5 ni 500 años. Limitar el rango reduce vectores de ataque imprevistos.

## 2. Salida de Datos Selectiva (Output Filtering)
Usa DTOs (Data Transfer Objects) para asegurar que el secreto de la empresa no sale por la API.
- **Tip Senior:** Crea un Pydantic base `PublicSchema` y hereda de él. Así te aseguras de que todos los modelos de salida siguen un estándar de privacidad.

## 3. Headers de Seguridad Automáticos
Usa middlewares para añadir cabeceras que activen las protecciones del navegador:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Content-Security-Policy: default-src 'none'; ...`

## 4. Desactivación de Servidor en Errores (Fail-Fast)
Si tu API detecta un intento de ataque obvio (ej: un SQL injection flagrante), no solo devuelvas un 400. Registra la IP y considera bloquearla temporalmente de forma automática.

## 5. Cifrado de Comunicaciones (TLS 1.3)
No permitas conexiones por protocolos antiguos como SSLv3 o TLS 1.0. Configura tu balanceador de carga o Nginx para que solo acepte TLS 1.2 o superior.

## 6. Manejo de Secretos en CI/CD
Asegúrate de que tus tests no necesiten secretos de producción. Usa "Mocks" o una base de datos de test efímera que se cree y borre en cada ejecución de la pipeline.

## Resumen: La seguridad es una característica, no un parche
Aplica estas mitigaciones como parte de tu definición de "Hecho" (Definition of Done). Un ticket no está terminado si no tiene validadores de entrada y si su esquema de salida no ha sido revisado para privacidad.
