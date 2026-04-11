# ¿Qué es MLOps?

**MLOps** (Machine Learning Operations) es un conjunto de prácticas que une el desarrollo de modelos (Machine Learning) con las operaciones de ingeniería (DevOps). Su objetivo es automatizar y estabilizar el ciclo de vida de los modelos en producción.

## 1. El problema: La "Deuda Técnica" de la IA
Crear un modelo en un Notebook es fácil. Mantenerlo funcionando de forma fiable en una empresa es muy difícil.
*   **DevOps:** Se centra en el código (binarios, scripts).
*   **MLOps:** Se centra en el **Código + Datos + Modelo**. Si uno de los tres cambia, todo el sistema cambia.

## 2. Los Pilares de MLOps

### A. Automatización (CI/CD/CT)
*   **CI (Integración Continua):** Pruebas automáticas del código y validación de los datos.
*   **CD (Despliegue Continuo):** Llevar el modelo a producción automáticamente.
*   **CT (Entrenamiento Continuo):** El sistema re-entrena el modelo solo cuando llegan nuevos datos.

### B. Reproducibilidad
Cualquier persona del equipo debe poder obtener el mismo modelo exacto que tú usando los mismos datos y el mismo código. Esto requiere control de versiones de ciencia de datos.

### C. Escalabilidad
Gestionar el entrenamiento de modelos pesados en clusters de servidores (Kubernetes) y responder a millones de peticiones por segundo en producción.

### D. Monitoreo y Gobernanza
Saber en cada momento qué modelo está en producción, con qué datos se entrenó y quién le dio permiso para desplegarse.

## 3. Niveles de Madurez MLOps (según Google)
*   **Nivel 0 (Manual):** Todo se hace en Notebooks, el despliegue es manual y no hay monitoreo.
*   **Nivel 1 (Automatización del Pipeline):** El entrenamiento es automático pero el despliegue sigue siendo controlado.
*   **Nivel 2 (Automatización CI/CD/CT):** Todo el flujo es automático, desde la llegada del dato hasta el despliegue del nuevo modelo. Es el "Estado del Arte".

## Resumen: DevOps para Inteligencia Artificial
MLOps no es una técnica, es una cultura de ingeniería aplicada a la IA. Permite que los modelos dejen de ser "proyectos de investigación" y se conviertan en servicios de software robustos, predecibles y escalables que la empresa puede usar con total confianza.
