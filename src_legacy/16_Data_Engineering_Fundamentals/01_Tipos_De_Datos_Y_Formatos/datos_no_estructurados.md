# Datos No Estructurados: El mar de información

Los datos no estructurados son información que no tiene un formato predefinido. Representan el 80% de los datos generados en el mundo hoy en día.

## 1. Ejemplos Reales
- **Texto Libre:** Emails, posts de redes sociales, documentos PDF.
- **Multimedia:** Imágenes, audio, vídeo.
- **Logs de Servidor:** Texto plano con marcas de tiempo pero sin estructura interna clara.

## 2. El reto del Procesamiento
No puedes hacer un `SELECT sum(ventas)` en una carpeta de vídeos. Para sacar valor de estos datos necesitamos técnicas avanzadas:
- **NLP (Procesamiento de Lenguaje Natural):** Para entender el sentimiento de un texto.
- **Computer Vision:** Para clasificar objetos en imágenes.
- **RegEx (Expresiones Regulares):** Para extraer patrones de logs de texto.

## 3. Dónde se guardan: Data Lakes
Como no tienen estructura, no se pueden meter en una base de datos SQL. Se guardan tal cual en sistemas de almacenamiento de archivos masivos como AWS S3 o Google Cloud Storage.

## 4. El valor oculto
Aunque son difíciles de procesar, contienen información riquísima. Analizar las grabaciones de llamadas de atención al cliente puede revelar más problemas que cualquier reporte de ventas estructurado.

## 5. El Ingeniero de Datos y la "Estructuración"
Nuestra misión a menudo es convertir este "caos" en algo estructurado. Ej: Construir un pipeline que lea logs de texto plano, extraiga la IP y el error, y lo guarde en una tabla limpia.

## Resumen: Capturar antes de Entender
En ingeniería de datos senior, la estrategia suele ser "guardar todo lo no estructurado hoy, porque mañana tendremos la tecnología para analizarlo y sacar valor".
