# Patrones de Ingesta: Push vs. Pull

A la hora de diseñar la entrada de datos, debes decidir quién tiene la iniciativa: ¿tu pipeline va a buscar el dato o el dato viene a ti?

## 1. Patrón PULL (Tu vas a buscar)
El pipeline se despierta (ej: por Airflow) y consulta la fuente.
- **Pros:** Tienes el control total de cuándo y cuánto procesas. No saturas el sistema de destino.
- **Contras:** Latencia (el dato espera en la fuente hasta que tú vas).
- **Uso:** APIs, Bases de datos, archivos FTP.

## 2. Patrón PUSH (El dato llega a ti)
La fuente envía el dato en cuanto lo genera.
- **Pros:** Latencia mínima. Reacción inmediata.
- **Contras:** El destino debe estar siempre listo. Si hay un pico masivo de datos, el destino puede morir por sobrecarga si no hay un buffer intermedio.
- **Uso:** Webhooks, Microservicios enviando a colas.

## 3. Full Refresh vs. Incremental
- **Full Refresh:** Borras todo y traes todo. Seguro, pero lento e ineficiente en tablas grandes.
- **Incremental:** Solo traes los cambios. Rápido y escalable, pero propenso a errores si pierdes el rastro de la última carga (Checkpoint).

## 4. Backfilling: Viajando al pasado
A veces descubres que un pipeline tenía un bug y los datos de los últimos 3 meses están mal.
- **Backfill** es la capacidad de re-ejecutar el pipeline para fechas pasadas de forma masiva.
- Tu patrón de ingesta debe permitir pasar un parámetro de fecha: `python ingest.py --start-date 2024-01-01`.

## 5. El concepto de "Idempotent Ingestion"
Independientemente del patrón, la ingesta debe poder repetirse 10 veces sin duplicar los datos. Esto se logra mediante el uso de IDs únicos y cargas de tipo "Overwrite" o "Upsert".

## Resumen: Elige tu Estrategia
El patrón **Pull** es el más seguro y fácil de empezar. El patrón **Push** es necesario cuando el negocio ya no puede esperar minutos y necesita segundos. Un Data Engineer Senior domina ambos y sabe cuándo aplicar cada uno.
