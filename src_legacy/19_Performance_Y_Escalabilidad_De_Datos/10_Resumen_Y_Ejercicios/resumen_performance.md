# Resumen y Ejercicios: Performance y Escalabilidad

¡Enhorabuena! Has completado el viaje por el rendimiento de los datos. Has aprendido que ser un buen ingeniero no es solo hacer que el código funcione, sino hacerlo escalar de forma eficiente y económica.

## 1. Resumen de Conceptos Clave

| Concepto | Definición Clave | Herramienta/Técnica |
| :--- | :--- | :--- |
| **Performance** | Eficiencia de una sola unidad (Velocidad). | SQL EXPLAIN, Profiling. |
| **Escalabilidad** | Capacidad de crecer añadiendo recursos. | Escalado Horizontal, Sharding. |
| **I/O Bound** | Cuello de botella en red o disco. | Caching, Asyncio, Batching. |
| **CPU Bound** | Cuello de botella en el procesador. | Multiprocessing, Algoritmos $O(n)$. |
| **Particionado** | División física de tablas gigantes. | Range/List/Hash Partitioning. |
| **Caching** | Atajo de datos en memoria RAM. | Redis, TTL, Cache-Aside. |
| **FinOps** | Responsabilidad financiera del Cloud. | Rightsizing, Spot Instances. |
| **Columnar** | Formato de datos para analítica masiva. | Parquet, BigQuery. |

## 2. Los 3 Pilares del Éxito
1.  **Mide antes de actuar:** No optimices por intuición. Usa `EXPLAIN ANALYZE` y métricas de CPU/RAM.
2.  **Diseña para el fallo:** Los sistemas masivos fallan; usa procesos idempotentes y reintentos.
3.  **Cuestiona el requerimiento:** A veces, el mayor ahorro de rendimiento es no procesar el dato que nadie mira.

---

## 3. Ejercicios Prácticos

### Ejercicio 1: El Sherlock Holmes del SQL
**Escenario:** Tienes una consulta que tarda 30 segundos en devolver los pedidos de un cliente. 
*   **Tarea:** Escribe los pasos que seguirías para identificar la causa usando `EXPLAIN`. ¿Qué buscarías exactamente en la salida del plan de ejecución?
*   **Bonus:** ¿Qué índice añadirías si detectas un "Sequential Scan" en la columna `customer_id`?

### Ejercicio 2: El Arquitecto del Caché
**Escenario:** Tu API de productos recibe 1.000 peticiones por segundo. La base de datos está al 95% de CPU.
*   **Tarea:** Diseña una estrategia de caché con Redis usando el patrón **Cache-Aside**.
*   **Pregunta:** ¿Qué TTL pondrías a un producto que cambia de stock cada hora? ¿Cómo invalidarías la caché si el precio cambia por sorpresa?

### Ejercicio 3: El Gestor de Presupuesto (FinOps)
**Escenario:** Tu pipeline de datos en Cloud Storage ocupa 10TB y cuesta 200$/mes. Sabes que el 80% de esos datos son logs de hace más de un año que nadie consulta.
*   **Tarea:** Define una política de **Ciclo de Vida (Lifecycle Policy)** para reducir la factura a la mitad sin borrar los datos (por si acaso).

### Ejercicio 4: Python a toda máquina
**Escenario:** Tienes que procesar 10.000 archivos JSON y extraer una métrica de cada uno. El script tarda 10 minutos.
*   **Tarea:** ¿Qué técnica usarías para aprovechar los 8 núcleos de tu CPU? Escribe un pequeño esquema de código usando `multiprocessing.Pool`.

---

## 4. Conclusión Final
El performance es un viaje, no un destino. Las tecnologías cambian, pero los principios de **eficiencia**, **simplicidad** y **escalabilidad** son universales. Sigue midiendo, sigue optimizando y, sobre todo, sigue pensando en grande.
