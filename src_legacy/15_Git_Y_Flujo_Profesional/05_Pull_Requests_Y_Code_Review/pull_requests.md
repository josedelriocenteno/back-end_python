# Pull Requests: Paso a Paso hacia el código compartido

La Pull Request (PR) es donde tu código se convierte en parte del producto. Es un proceso de control de calidad y aprendizaje compartido.

## 1. El ciclo de vida de una PR
1. **Push:** Envías tu rama `feature` al remoto.
2. **Open:** Creas la PR en GitHub.
3. **Review:** Tus compañeros comentan y sugieren cambios.
4. **Update:** Haces los cambios solicitados y pusheas de nuevo (la PR se actualiza sola).
5. **Approval:** Recibes el "LGTM" (Looks Good To Me).
6. **Merge:** El código se integra en `main`.

## 2. Anatomía de la PR Perfecta
- **Título descriptivo:** `feat(auth): añadido soporte para OAuth2 con Google`.
- **Contexto:** ¿Por qué es necesario este cambio? ¿Qué bug resuelve?
- **Instrucciones de prueba:** ¿Cómo puede el revisor verificar que esto funciona?
- **Capturas de pantalla / Videos:** Si hay cambios visuales, son imprescindibles.

## 3. Draft Pull Requests (Borradores)
Si tu trabajo no está terminado pero quieres feedback temprano:
- Publica tu PR como **Draft**.
- Esto indica que no está lista para mergear pero permite que otros vean tu progreso y opinen sobre la arquitectura.

## 4. Diferencias entre Merge y Squash en PRs
Al cerrar una PR, GitHub ofrece:
- **Merge Commit:** Crea un commit de unión (Mantiene historial detallado).
- **Squash and Merge:** Aplasta todos los commits de la PR en uno solo (Limpia `main`).
- **Rebase and Merge:** Mueve los commits de la PR al final de `main` (Historial lineal).

## 5. El valor de la conversación
Una PR es una herramienta de comunicación. Participar activamente en los hilos de conversación de tu PR demuestra compromiso y capacidad de trabajar en equipo.

## Resumen: Calidad por encima de todo
Una PR no es un trámite molesto; es el momento en que el equipo asegura que el repositorio se mantiene sano y que todos aprenden de las soluciones de los demás.
