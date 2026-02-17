# Caching de Dependencias: Acelerando el flujo de trabajo

Esperar 10 minutos a que Docker instale Pandas y NumPy cada vez que cambias un `print("Hola")` es inaceptable. El caching inteligente es lo que separa a un desarrollador productivo de uno frustrado.

## 1. La Ley del Cambio Poco Frecuente
En Docker, los archivos que cambian menos deben estar más arriba en el Dockerfile.
- **Frecuencia muy baja:** El SO (`FROM python`).
- **Frecuencia baja:** Los instaladores de librerías (`pip install`).
- **Frecuencia alta:** Tu código fuente (`COPY . .`).

## 2. El truco del "Split Copy"
Nunca hagas `COPY . .` antes de instalar dependencias.
```dockerfile
# BIEN:
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . # Si el código cambia, la línea de arriba NO se vuelve a ejecutar.
```

## 3. Docker BuildKit y Mount Caches (Avanzado)
Desde Docker 18.09, puedes usar caches de montaje persistentes que sobreviven entre builds, igual que hace tu ordenador local con la carpeta `~/.cache/pip`.

```dockerfile
# Uso de cache persistente para Pip (BuildKit requerido)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```
- **Ventaja:** Si añades una sola librería nueva, Docker no bajará las otras 49 de nuevo; las leerá del cache de montaje.

## 4. Multistage Caching
Si usas multi-stage builds, puedes cachear la etapa de `builder` por separado. En el CI (GitHub Actions), esto ahorra una cantidad masiva de tiempo al no tener que recompilar drivers de DB en cada commit.

## Resumen: Tiempo es Dinero
Un pipeline de CI/CD optimizado con buen caching puede tardar 1 minuto. Uno mal diseñado puede tardar 15. En un equipo de 10 desarrolladores, esa diferencia de tiempo se traduce en miles de euros de productividad ganada al mes.
