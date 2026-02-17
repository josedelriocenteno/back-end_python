# Aprendizaje No Supervisado: Encontrando el orden oculto

En el **Aprendizaje No Supervisado**, le damos al algoritmo los datos pero **NO le damos las etiquetas**. El sistema debe explorar los datos por su cuenta y encontrar estructuras, similitudes o patrones que nosotros no habíamos visto.

## 1. ¿Cómo funciona?
El modelo analiza las características de los datos y agrupa aquellos que se parecen entre sí. No sabe qué son los datos, solo sabe que "estos se parecen y aquellos son diferentes".

## 2. Los dos problemas principales

### A. Clustering (Agrupamiento)
Divide los datos en grupos basados en similitudes.
*   **Ejemplo:** Tienes 1 millón de clientes pero no sabes cómo dividirlos. El algoritmo los agrupa por "comportamiento de gasto" y "frecuencia".
*   **Resultado:** Descubres un grupo de "Ahorradores" y otro de "Compradores Impulsivos" que no sabías que existían.

### B. Asociación
Encuentra reglas que describen grandes conjuntos de datos.
*   **Ejemplo:** "Las personas que compran pañales también tienden a comprar cerveza los viernes por la tarde".
*   **Uso:** Sistemas de recomendación de Amazon o colocación de productos en supermercados.

## 3. Reducción de Dimensionalidad
A veces tenemos demasiados datos (1.000 columnas). El aprendizaje no supervisado ayuda a comprimir esa información en 3 o 4 columnas esenciales sin perder la esencia del patrón. (Ej: algoritmo PCA).

## 4. Algoritmos Comunes
*   **K-Means:** El rey del agrupamiento (Clustering).
*   **DBSCAN:** Encuentra grupos de formas irregulares.
*   **PCA (Principal Component Analysis):** Para comprimir datos.

## 5. ¿Para qué sirve realmente?
Es ideal para la **fase de exploración**. Antes de intentar predecir algo, usamos aprendizaje no supervisado para entender qué tipos de datos tenemos y qué grupos naturales se forman.

## Resumen: El detective de datos
El aprendizaje no supervisado es como soltar a un científico en un planeta desconocido: no sabe los nombres de las plantas ni de los animales, pero puede empezar a agrupar los que tienen hojas de los que tienen pelo. Es la clave para descubrir oportunidades de negocio ocultas en tus datos.
