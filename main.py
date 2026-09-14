from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, Base, get_db

# Crea físicamente las tablas en SQLite al arrancar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ABM de Productos")

@app.post("/productos/", response_model=schemas.ProductoResponse, status_code=status.HTTP_201_CREATED) 
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db) ): #Conexion a pydantic y tira 442 si no cumple
    return crud.crear_producto(db=db, producto=producto)

@app.get("/productos/", response_model=List[schemas.ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_productos(db=db, skip=skip, limit=limit)

@app.get("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def obtener_producto_por_id(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.obtener_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="El producto no fue encontrado")
    return db_producto

@app.put('/productos/{producto_id}', response_model= schemas.ProductoResponse)
def modificar_producto(producto_id: int, producto_data: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = crud.actualizar_producto(db=db, producto_id=producto_id, producto_data=producto_data)
    if db_producto is None: 
        raise HTTPException(status_code=404, detail='El producto no fue encontrado')
    return db_producto     

@app.delete("/productos/{producto_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_producto(db=db, producto_id=producto_id)
    if not exito:
        raise HTTPException(status_code=404, detail="El producto no fue encontrado para eliminar")
    return {"mensaje": f"El producto con ID {producto_id} ha sido eliminado correctamente"}

# ------------------------------------------------------------------
# ENDPOINTS PARA VENTAS
# ------------------------------------------------------------------

# 1. ALTA (Crear Venta)
@app.post(
    "/ventas/", 
    response_model=schemas.VentaResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["Ventas"]
)
def crear_venta(
    venta: schemas.VentaCreate, 
    db: Session = Depends(get_db)
):
    # Opcional: Validar que el producto exista antes de procesar la venta
    db_producto = crud.obtener_producto(db, producto_id=venta.id_producto)
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El producto asociado a la venta no existe"
        )
    
    return crud.crear_venta(db=db, venta=venta)


# 2. CONSULTA GENERAL (Obtener listado de ventas)
@app.get(
    "/ventas/", 
    response_model=List[schemas.VentaResponse],
    tags=["Ventas"]
)
def listar_ventas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud.obtener_ventas(db=db, skip=skip, limit=limit)


# 3. CONSULTA POR ID (Obtener una venta específica)
@app.get(
    "/ventas/{venta_id}", 
    response_model=schemas.VentaResponse,
    tags=["Ventas"]
)
def obtener_venta(
    venta_id: int, 
    db: Session = Depends(get_db)
):
    db_venta = crud.obtener_venta(db=db, venta_id=venta_id)
    if db_venta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La venta solicitada no existe"
        )
    return db_venta


# 4. MODIFICACIÓN PARCIAL (Actualizar datos de una venta)
@app.put(
    "/ventas/{venta_id}", 
    response_model=schemas.VentaResponse,
    tags=["Ventas"]
)
def actualizar_venta(
    venta_id: int, 
    venta_update: schemas.VentaUpdate, 
    db: Session = Depends(get_db)
):
    db_venta = crud.actualizar_venta_parcial(
        db=db, 
        venta_id=venta_id, 
        venta_data=venta_update
    )
    if db_venta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontró la venta para actualizar"
        )
    return db_venta


# 5. BAJA (Eliminar Venta)
@app.delete(
    "/ventas/{venta_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Ventas"]
)
def eliminar_venta(
    venta_id: int, 
    db: Session = Depends(get_db)
):
    exito = crud.eliminar_venta(db=db, venta_id=venta_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La venta que intentas eliminar no existe"
        )
    return None