# Instalación y Setup Profesional de FastAPI

FastAPI no es solo una librería; es un ecosistema. Para empezar con el pie derecho, debemos configurar un entorno de desarrollo reproducible y robusto.

## 1. El Core de FastAPI
Para que FastAPI funcione, necesitamos tres componentes principales:
1.  **FastAPI:** El framework web.
2.  **Uvicorn:** El servidor ASGI (Asynchronous Server Gateway Interface) que ejecuta la app.
3.  **Pydantic:** (Instalado con FastAPI) Se encarga de la validación de datos.

## 2. Instalación con Poetry (Recomendado)
Poetry es el estándar moderno en la industria para gestionar dependencias. Evita el infierno de versiones y bloquea el entorno.

```bash
# Inicializar proyecto
poetry init

# Añadir FastAPI y servidor
poetry add fastapi uvicorn[standard]

# Añadir herramientas de testing (solo desarrollo)
poetry add --group dev pytest httpx
```

## 3. ¿Por qué `uvicorn[standard]`?
Al añadir `[standard]`, Uvicorn instala dependencias extra como `uvloop` (un event loop de alto rendimiento escrito en C) y `httptools` (un parser de HTTP extremadamente rápido). Esto es vital para exprimir al máximo el rendimiento de Python.

## 4. Estructura de un Entorno Virtual (venv)
Si prefieres no usar Poetry, usa al menos `venv` de forma manual:
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]"
```

## 5. El archivo `.gitignore` esencial
Nunca subas tu entorno virtual o archivos de configuración locales a Git. Tu `.gitignore` debe incluir:
```text
.venv/
__pycache__/
.env
.pytest_cache/
```

## 6. Verificando la instalación
Puedes comprobar que todo está listo lanzando el comando de ayuda de uvicorn:
`uvicorn --help`

## Resumen: Los cimientos de tu API
La calidad de tu software empieza por cómo gestionas sus dependencias. Un entorno limpio y controlado con Poetry o venv te asegura que si tu código corre hoy, correrá igual en producción mañana.
