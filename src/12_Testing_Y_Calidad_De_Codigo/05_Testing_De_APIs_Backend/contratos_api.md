# Contratos de API: La Promesa entre Equipos

En una arquitectura de microservicios o en un equipo con frontend y backend separados, el **Contrato de API** es el documento que dice qué datos se envían y se reciben. Testing de contratos (Consumer-Driven Contracts) es la forma de asegurar que nadie rompe la App de los demás.

## 1. OpenAPI (Swagger) como Única Verdad
En FastAPI, el contrato se genera automáticamente en `/openapi.json`.
- **Test de Senior:** Puedes crear un test que compare el archivo `openapi.json` actual con una versión "maestra" guardada en el repositorio. Si el archivo cambia, el test falla y obliga al desarrollador a documentar el cambio o revertirlo.

## 2. Breaking Changes (Cambios Rompedores)
Un cambio rompedor es:
- Borrar un campo del JSON de respuesta.
- Cambiar un tipo (de `int` a `str`).
- Hacer obligatorio un parámetro que antes era opcional.
- Cambiar el status code de éxito (de 200 a 201 podría romper algunos clientes muy rígidos).

## 3. Postman y Newman
Aunque Pytest es el rey, a veces los equipos de QA prefieren usar Postman.
- **Newman** es la herramienta de línea de comandos que permite ejecutar colecciones de Postman dentro de tu pipeline de CI/CD. Es útil para tests E2E y de integración "caja negra".

## 4. Schemathesis: Testing de Propiedades
Es una herramienta increíble para Python que lee tu archivo `openapi.json` y genera automáticamente MILES de tests buscando fallos en tu API:
- Envía strings gigantes.
- Envía tipos de datos incorrectos.
- Intenta romper tus validaciones enviando valores límite.
- **Detecta:** Errores 500 no capturados que reveals información interna.

## 5. Documentación vs Realidad
El mayor pecado es que la documentación diga una cosa y la API haga otra. 
- **Solución:** Los tests de respuesta que vimos en el archivo anterior (`validacion_respuestas.py`) deben usar los MISMOS modelos Pydantic que usa la API para su documentación. Así, la coherencia está garantizada por código.

## Resumen: Sin sorpresas
Un contrato de API sólido permite que el equipo de frontend trabaje con total confianza sabiendo que el backend no va a cambiar un campo sin avisar. Los tests de contrato son la herramienta de comunicación más potente entre departamentos técnicos.
