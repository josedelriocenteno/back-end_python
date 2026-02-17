# Imagen vs. Contenedor: El gran salto conceptual

Una de las mayores confusiones al empezar con Docker es no distinguir entre estos dos conceptos. Es clave para entender cómo escalar aplicaciones.

## 1. La Imagen (The Blueprint)
Es un archivo estático, de solo lectura, que contiene TODO lo que tu aplicación necesita:
- El código fuente.
- El intérprete de Python.
- Las librerías (`requirements.txt`).
- Variables de entorno por defecto.
- El comando de arranque.

**Piensa en ella como:**
- Una Clase en programación POO.
- Una receta de cocina escrita en un libro.
- Un instalador de un programa (.exe o .dmg).

## 2. El Contenedor (The Instance)
Es la imagen en ejecución. Es un proceso vivo que tiene su propio sistema de archivos (una copia escribible sobre la imagen) y su propia red.

**Piensa en él como:**
- Un Objeto (instancia de la clase).
- El plato de comida ya cocinado sobre la mesa.
- El programa ya abierto y corriendo en tu monitor.

## 3. Relación 1:N
De una sola imagen (ej: `python-backend:v1`) puedes lanzar 1, 10 o 100 contenedores idénticos al mismo tiempo. Todos compartirán la misma base de "solo lectura", pero cada uno tendrá su propia memoria y estado efímero.

## 4. Inmutabilidad (Crucial para Senior)
Las imágenes son **inmutables**. Si quieres cambiar una línea de código:
1. No entras al contenedor a editarla.
2. Editas el código en tu host.
3. Generas una **NUEVA imagen**.
4. Borras el contenedor viejo y lanzas uno nuevo con la imagen actualizada.

## Resumen: Estático vs Dinámico
- **Imagen:** Lo que construyes y subes al servidor.
- **Contenedor:** Lo que consume CPU y RAM y sirve peticiones a tus usuarios.
