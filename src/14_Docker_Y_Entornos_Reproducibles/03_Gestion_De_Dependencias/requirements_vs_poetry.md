# Requirements.txt vs Poetry en Docker

Muchos desarrolladores se preguntan si merece la pena pasar de los clásicos `requirements.txt` a Poetry cuando ya estás usando contenedores. Aquí la comparativa desde una perspectiva de arquitectura.

## 1. Requirements.txt (El enfoque clásico)
- **Pro:** Simplicidad absoluta. Se instala con un simple `pip install`. Las imágenes base de Python están optimizadas para esto.
- **Contra:** No gestiona bien las dependencias de las dependencias (transitive dependencies). Si una librería actualiza una dependencia interna, tu build puede romperse sin aviso.
- **Uso ideal:** Scripts pequeños, microservicios ultra-simples o APIs donde la velocidad del build es crítica y las dependencias son muy pocas.

## 2. Poetry / Conda / PDM (Gestores Modernos)
- **Pro:** El archivo de "lock" (`poetry.lock`). Garantiza que el árbol de dependencias sea siempre el mismo. Proporciona una resolución de conflictos mucho más inteligente.
- **Contra:** Añade complejidad al Dockerfile. Tienes que instalar el gestor primero, lo que aumenta un poco el tiempo de build inicial y el tamaño de la imagen.
- **Uso ideal:** Proyectos medianos y grandes, Data Pipelines con muchas librerías científicas, y entornos donde la reproducibilidad es moneda de cambio.

## 3. El error de mezclar ambos
Exportar de Poetry a `requirements.txt` solo para construir el Dockerfile es un anti-patrón común.
- **Peligro:** Estás perdiendo los metadatos de Poetry y añadiendo un paso manual que alguien olvidará actualizar algún día.
- **Solución:** Si usas Poetry, úsalo directamente en el Dockerfile como vimos en la sección anterior.

## Resumen: Seguridad sobre Velocidad
Para un entorno backend corporativo, **Poetry gana**. La seguridad de saber que tu build no se romperá un domingo por la noche porque una librería en la otra punta del mundo se actualizó no tiene precio.
