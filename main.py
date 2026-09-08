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

@app.put('/productos/{producto_id}', response_model= schemas.ProductoUpdate)
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