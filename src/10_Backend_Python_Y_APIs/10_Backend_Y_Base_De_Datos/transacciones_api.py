"""
BACKEND + DB: TRANSACCIONES Y CONSISTENCIA
-----------------------------------------------------------------------------
Asegurar que un proceso complejo (ej: un pedido con muchos items) se guarde 
entero o no se guarde nada (Todo o Nada).
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db_dependency import get_db

app = FastAPI()

@app.post("/orders/")
def create_order(items: list, db: Session = Depends(get_db)):
    """
    Ejemplo de una transacción que afecta a múltiples tablas.
    """
    try:
        # 1. Iniciar la orden principal
        order = Order(total=100.0)
        db.add(order)
        db.flush() # flush() envía los datos a la DB pero SIN confirmar el commit.
        # Esto genera el ID de la orden para poder usarlo en los items.

        # 2. Crear los items vinculados
        for item_data in items:
            new_item = OrderItem(order_id=order.id, **item_data)
            db.add(new_item)
            
            # Simulamos un error de stock en el tercer item
            if item_data["qty"] > 100:
                raise ValueError("No hay stock suficiente")

        # 3. Confirmación final
        db.commit() # Solo si llegamos aquí, se guardan la orden Y todos los items.
        return {"id": order.id, "status": "Order saved"}

    except Exception as e:
        # 4. En caso de CUALQUIER error, volvemos atrás
        db.rollback() # Limpia lo que se intentó guardar (Orden e items previos)
        raise HTTPException(status_code=400, detail=f"Error en la transacción: {e}")

"""
DIFERENCIA ENTRE FLUSH Y COMMIT:
-----------------------------------------------------------------------------
- FLUSH: Sincroniza el estado de la memoria con la DB (ej: genera IDs), pero 
  la transacción sigue ABIERTA y bloquea filas.
- COMMIT: Cierra la transacción y hace que los cambios sean visibles para 
  todos los demás usuarios.

RESUMEN:
Usa siempre un bloque try/except con db.rollback() cuando operes sobre 
más de una fila a la vez para evitar dejar la base de datos en un estado 
inconsistente ("Corrupto").
"""
