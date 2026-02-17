# ¿Qué es Git y por qué existe?

Git es un **Sistema de Control de Versiones Distribuido (DVCS)**. Su propósito es rastrear cambios en el código fuente durante el desarrollo de software y permitir que varios desarrolladores trabajen juntos de forma eficiente.

## 1. El problema antes de Git
Sin control de versiones, los equipos recurrían a:
- Copiar carpetas (`proyecto_final_v1`, `proyecto_final_v2_este_si`).
- Comentar código viejo por si acaso.
- Gritarse a través de la oficina: "¿Quién está tocando el archivo `main.py`?".

## 2. Cómo piensa Git: Instantáneas (Snapshots)
A diferencia de otros sistemas que guardan "diferencias" entre archivos, Git toma una **foto completa** del estado de tu proyecto en cada commit.
- Si un archivo no ha cambiado, Git simplemente guarda un enlace al archivo anterior para ahorrar espacio.

## 3. Arquitectura Distribuida
"Distribuido" significa que cada desarrollador tiene una copia **completa** del historial del proyecto en su ordenador. 
- Puedes trabajar sin internet.
- Si el servidor central explota, cualquiera puede restaurar el proyecto completo.

## 4. Rapidez y Seguridad
Git es extremadamente rápido porque casi todas las operaciones son locales. Además, utiliza un sistema de **Hash (SHA-1)** para asegurar la integridad de los datos: es imposible cambiar un byte del pasado sin que Git se dé cuenta.

## Resumen: La máquina del tiempo
Git es la infraestructura que te permite fallar, experimentar y colaborar con la seguridad de que siempre puedes volver atrás y de que nada se pierde por accidente.
