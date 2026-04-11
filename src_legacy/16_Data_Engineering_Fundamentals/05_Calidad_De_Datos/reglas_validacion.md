# Reglas de Validación: Tu escudo protector

Las reglas de validación son los "tests unitarios" de tus datos. Deben ejecutarse en cada paso del pipeline.

## 1. Validaciones de Estructura
Asegurar que el "contenedor" es correcto:
- ¿Están todas las columnas obligatorias?
- ¿Los nombres de las columnas han cambiado?
- ¿El tipo de dato es el esperado (Int vs String)?

## 2. Validaciones de Valor
Asegurar que el "contenido" tiene sentido:
- **Null Checks:** ¿Hay campos obligatorios vacíos?
- **Range Checks:** ¿La edad está entre 0 y 120? ¿El precio es positivo?
- **Pattern Checks:** ¿El email tiene formato de email? ¿El código postal tiene 5 dígitos?

## 3. Validaciones de Negocio
Suelen requerir consultar otros datos:
- ¿El ID del producto existe en nuestra tabla maestra de productos?
- ¿La fecha de entrega es posterior a la fecha de pedido?

## 4. Implementación en Python (Pydantic / Pandera)
No escribas `if/else` infinitos. Usa librerías:
```python
# Ejemplo con Pandera para validar un DataFrame de Pandas
import pandera as pa

schema = pa.DataFrameSchema({
    "user_id": pa.Column(int, unique=True),
    "email": pa.Column(str, checks=pa.Check.str_matches(r".+@.+\..+")),
    "age": pa.Column(int, checks=pa.Check.in_range(0, 120))
})
schema.validate(df)
```

## 5. El criterio de parada
- **Soft Validation:** El error se loguea pero el pipeline sigue. Útil para datos "deseables" pero no críticos.
- **Hard Validation:** Si falla la validación, el pipeline se para. Obligatorio para datos que rompen los sistemas de destino.

## Resumen: Prevención Proactiva
Las reglas de validación detectan errores en la frontera. Es mucho más barato detectar un error cuando el dato entra que intentar arreglarlo meses después cuando ya está en un reporte de ventas.
