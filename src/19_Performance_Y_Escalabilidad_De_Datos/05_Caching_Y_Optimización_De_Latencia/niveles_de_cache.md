# Niveles de Caché: De la CPU al Cliente

La caché no ocurre en un solo sitio. Un sistema moderno tiene múltiples "paradas" donde el dato puede estar guardado para ahorrar tiempo.

## 1. Caché de CPU (L1/L2/L3)
*   Integrada en el propio procesador. Gestionada automáticamente por el hardware.
*   Es la más rápida del mundo, pero muy pequeña (MB).

## 2. Caché de Aplicación (Local Cache)
*   Guardada en la memoria RAM del servidor donde corre tu código (Python, Node).
*   **Pros:** Latencia cero (está en el mismo proceso).
*   **Contras:** Si tienes 10 servidores, cada uno tiene su propia caché y pueden estar descoordinados. Se pierde al reiniciar la App.

## 3. Caché Distribuida (Redis, Memcached)
*   Un servidor independiente dedicado exclusivamente a guardar datos en RAM.
*   **Pros:** Todos tus servidores de aplicaciones consultan la misma caché centralizada. Los datos sobreviven si reinicias la App.
*   **Contras:** Añade un pequeño retraso de red (1-2ms), pero sigue siendo mucho más rápido que la base de datos.

## 4. Caché de Base de Datos (Buffer Pool)
*   Las bases de datos (Postgres, MySQL) guardan automáticamente las últimas páginas de datos leídas de disco en su memoria RAM.
*   **Tip:** Si tienes mucha RAM en tu base de datos, ¡esta caché hará que tus queries parezcan mágicamente rápidas!

## 5. Caché de Red y CDN (Edge Cache)
*   **Content Delivery Network:** Guarda copias de tus archivos (imágenes, JSON de API) en servidores repartidos por todo el mundo.
*   **Ventaja:** Si un usuario de Japón pide una imagen a tu servidor de España, la CDN se la sirve desde un servidor en Tokio en milisegundos.

## 6. Caché de Navegador
*   El propio navegador del usuario guarda archivos estáticos basándose en cabeceras HTTP (`Cache-Control`).

## Resumen: Defensa en Profundidad
Diseñar para el rendimiento es colocar capas de caché estratégicas. Cuanto más cerca del usuario esté el dato, mejor será la experiencia. Como ingeniero, debes decidir qué nivel aporta más valor en cada caso sin añadir una complejidad innecesaria.
