# Detección de Fallos Silenciosos: El peor enemigo

Un fallo silencioso ocurre cuando tu sistema dice que "todo ha ido bien" (Código 0), pero los datos son incorrectos. Es el problema más difícil de detectar y el más peligroso.

## 1. Ejemplos de Fallos Silenciosos
*   **El API mentirosa:** Un endpoint devuelve un 200 OK pero el JSON está vacío `{}`.
*   **El esquema fantasma:** Una columna de fecha cambia de formato (`YYYY-MM-DD` a `DD/MM/YYYY`) y el parser de Python pone `NULL` en todas las filas sin dar error.
*   **La caída parcial:** Se procesan 10 archivos de 1.000 correctamente, pero se ignoran sin aviso otros 500 archivos.

## 2. Cómo detectarlos con Observabilidad
*   **Invariant Checks:** Define reglas que SIEMPRE deben cumplirse. "La suma de las ventas nunca puede ser negativa". Si se rompe, el sistema avisa.
*   **Anomaly Detection de Volumen:** Si el volumen de datos de hoy se desvía más de un 30% de la media de los últimos 7 días, lanza una alerta.
*   **Schema Drift Detection:** Monitoriza si el número de columnas o sus tipos cambian entre una ejecución y otra.

## 3. Auditoría e Integridad
*   **Checksums:** Compara el tamaño o el hash del dato en origen y en destino.
*   **Record Count Reconcile:** Siempre cuenta cuántas filas entran al pipeline y cuántas salen. Si `entran != (salen + descartadas)`, hay una fuga de datos.

## 4. El valor de los "Nulos"
Monitoriza el porcentaje de nulos por columna. 
- Si normalmente la columna `ciudad` tiene un 5% de nulos y de repente sube al 80%, el sistema de origen ha dejado de enviar ese dato, aunque el pipeline siga funcionando "técnicamente".

## 5. Alertas de Negocio (Business Alerts)
A veces el sistema está perfecto, pero el dato no tiene sentido. 
- Ejemplo: "Ningún usuario ha comprado nada en la última hora". Técnicamente todo funciona, pero comercialmente es imposible. Alertar sobre esto salva empresas.

## Resumen: Desconfianza Saludable
Un Data Engineer profesional nunca se fía de un "Success". Construye sistemas de auditoría paralelos que verifiquen constantemente que el resultado final tiene sentido lógico y matemático, sacando a la luz los fallos que intentan esconderse.
