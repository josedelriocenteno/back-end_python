# Errores Frecuentes del Data Engineer Junior

Todos hemos sido Juniors y todos hemos cometido estos errores. Conocerlos de antemano es como tener un mapa de un campo de minas.

## 1. Ignorar la Idempotencia
- **Error:** Escribir un script que si lo lanzas dos veces, inserta los datos dos veces.
- **Solución Senior:** Usa siempre `WRITE_TRUNCATE` para cargas de staging o lógica de "borrar datos del día antes de insertar" para asegurar que el resultado sea siempre el mismo independientemente de cuántas veces corra el pipeline.

## 2. No gestionar bien los Nulos
- **Error:** Confiar en que "la API siempre envía el nombre".
- **Consecuencia:** Tu pipeline falla el domingo a las 3 AM porque un usuario nuevo no puso su apellido.
- **Solución Senior:** Maneja excepciones y pon valores por defecto (`'Unknown'`, `0`) siempre que sea posible. Los datos del mundo real nunca son perfectos.

## 3. Olvidar limpiar después de trabajar
- **Error:** Crear una tabla temporal llamada `borrame_luego` o un Bucket de pruebas `test_123` y dejarlo ahí para siempre.
- **Consecuencia:** A final de año tu empresa paga miles de euros por basura.
- **Solución Senior:** Pon siempre fecha de expiración a tus tablas de prueba y limpia los buckets temporales.

## 4. No documentar el "Linaje"
- **Error:** Crear una tabla maravillosa en BigQuery pero no decirle a nadie de dónde viene ni qué significa la columna `status_id = 4`.
- **Solución Senior:** Usa las descripciones de tablas y columnas en BigQuery. Si no está documentado, el dato no existe para el resto de la empresa.

## 5. El "Scriptismo"
- **Error:** Escribir scripts de 2.000 líneas que solo tú entiendes.
- **Solución Senior:** Modulariza. Divide tu código en: `extractor.py`, `transformer.py` y `loader.py`. Usa funciones cortas y pon comentarios que expliquen la lógica de negocio, no solo lo que hace el código.

## Resumen: Actitud sobre Aptitud
Ser un buen Junior no es saberse todos los comandos de memoria, es ser ordenado, precavido y entender que tus pipelines van a ser mantenidos por otras personas en el futuro. Escribe código para que tu compañero te quiera, no para que te necesite.
