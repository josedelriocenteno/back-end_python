# ¿Qué son las Features (Atributos)?

En Machine Learning, una **Feature** (Atributo o Característica) es una propiedad individual medible o una característica de un fenómeno que se está observando. Es la información técnica que el modelo procesa para dar una respuesta.

## 1. El lenguaje del modelo
Los algoritmos no entienden "clientes", "fotos" o "ventas"; entienden vectores de números. La **Ingeniería de Atributos** es el arte de transformar los datos brutos en esos números de la forma que más ayude al modelo a encontrar el patrón.

## 2. Tipos de Features

### A. Numéricas
Valores cuantitativos.
*   **Continuas:** Pueden tomar cualquier valor (ej: precio, temperatura, peso).
*   **Discretas:** Valores enteros (ej: número de hijos, cantidad de productos comprados).

### B. Categóricas
Valores cualitativos o etiquetas.
*   **Nominales:** Sin un orden intrínseco (ej: Color, Ciudad, Género).
*   **Ordinales:** Tienen un orden lógico (ej: Nivel de estudios: Primaria < Secundaria < Universidad).

### C. Temporales
Fechas y horas. Muy raras de usar directamente; se suelen transformar en "Día de la semana", "¿Es festivo?", "Mes", etc.

## 3. Calidad sobre Cantidad
Tener 1.000 features no garantiza un modelo mejor. De hecho, a menudo es peor (visto en el tema anterior como el problema del ruido).
*   **Selección de Atributos:** Elegir solo los que aportan información real.
*   **Importancia de Atributos:** Medir qué columna está ayudando más al modelo a acertar.

## 4. El impacto en el negocio
Un modelo complejo con datos brutos suele rendir peor que un modelo sencillo con **features inteligentes**. 
*   **Ejemplo:** En lugar de darle al modelo la `fecha_nacimiento`, dale la `edad_actual`. Es un cálculo simple que le ahorra al modelo tener que descubrir la aritmética del tiempo por su cuenta.

## Resumen: Los ladrillos del conocimiento
Las features son los ladrillos con los que construyes tu modelo. Una mala elección de materiales hará que el edificio se caiga por muy bueno que sea el arquitecto (el algoritmo). Dominar la identificación y creación de atributos es la habilidad más valiosa de un profesional de los datos.
