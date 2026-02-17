# Estructura de Repo Profesional: Monorepo vs. Multirepo

Cómo organizas tus repositorios afecta a la cultura del equipo y a la arquitectura de tu software.

## 1. Multirepo (Un repo por servicio)
Es el estándar para microservicios.
- **Pro:** Aislamiento total. Puedes usar diferentes lenguajes y librerías en cada uno. Permisos granulares.
- **Contra:** Difícil gestionar cambios que afectan a varios servicios. Duplicidad de código de configuración (linters, CI/CD).

## 2. Monorepo (Todo en un solo repo gigante)
No confundir con un "monolito". El código está separado en carpetas pero vive en el mismo proyecto de Git.
- **Pro:** Refactorización atómica (un solo commit cambia el cliente y el servidor). Una sola configuración de herramientas.
- **Contra:** El repo puede pesar GBs. Git se vuelve lento. Requiere herramientas complejas para descargar solo lo necesario (Sparse Checkout).

## 3. Estructura de carpetas recomendada
Independientemente del modelo, un repo profesional suele verse así:
```text
/
├── apps/ (servicios o aplicaciones)
├── libs/ (código compartido)
├── docs/ (documentación extensa)
├── scripts/ (utilidades de build/deploy)
├── .github/ (workflows y acciones)
├── .gitignore
├── README.md
└── docker-compose.yml
```

## 4. Submódulos de Git (`git submodule`)
Permiten meter un repositorio dentro de otro.
- **Uso:** Cuando necesitas una librería externa de la que quieres el código fuente pero no quieres copiarlo físicamente.
- **⚠️ Cuidado:** Son difíciles de gestionar y suelen causar confusión en el equipo. Úsalos solo como último recurso.

## 5. El README es la entrada
Un repositorio sin un buen README es un repositorio invisible. Debe incluir:
- Qué hace el proyecto.
- Cómo instalarlo localmente.
- Cómo correr los tests.

## Resumen: Orden antes que Código
La estructura de tu repositorio es la interfaz de usuario para otros desarrolladores. Hazla coherente, predecible y documentada.
