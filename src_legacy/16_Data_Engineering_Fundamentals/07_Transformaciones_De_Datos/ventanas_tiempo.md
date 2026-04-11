# Ventanas de Tiempo: El contexto temporal

En el mundo del dato, el "cuándo" suele ser tan importante como el "qué". Las ventanas de tiempo nos permiten analizar tendencias y comportamientos a lo largo de un eje temporal.

## 1. Time-Series Analysis
Analizar cómo cambia un valor segundo a segundo o día a día.
- **Cálculos acumulados (Running Totals):** Cuánto llevamos vendido desde el 1 de Enero hasta hoy, actualizado en cada fila.
- **Comparativas (Year-over-Year):** ¿Estamos vendiendo más hoy que el mismo día del año pasado?

## 2. Funciones de Ventana (Window Functions) en SQL
Es la herramienta favorita de los ingenieros senior. Permite calcular sobre un conjunto de filas relacionadas con la fila actual sin perder el detalle del registro.
```sql
SELECT 
  user_id, 
  order_date, 
  amount,
  AVG(amount) OVER(PARTITION BY user_id ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg
FROM orders
```

## 3. Sesiones de Usuario
¿Qué hizo el usuario desde que entró en la web hasta que salió?
- Crear un `session_id` que agrupe todos los eventos que ocurren dentro de un margen de 30 minutos de inactividad.

## 4. Filtrado de ruido temporal
A veces los datos tienen "picos" que no representan la realidad (un sensor que falla un segundo). Usamos filtros de ventana (medias móviles) para suavizar la curva y ver la tendencia real.

## 5. El reto del "Late Data"
En Big Data, los datos pueden llegar tarde. Tu lógica de ventana debe decidir si acepta el dato de las 10:00 que ha llegado a las 11:00 o lo descarta.

## Resumen: La cuarta dimensión
Dominar las funciones de ventana y el análisis temporal permite responder preguntas complejas sobre el comportamiento de los usuarios y la salud del negocio que un simple `GROUP BY` no puede alcanzar.
