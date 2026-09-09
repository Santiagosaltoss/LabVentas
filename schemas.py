from pydantic import BaseModel
from typing import Optional 

class ProductoBase(BaseModel): #Base comun para todos los campos
    nombre: str
    id: int 
    precio: float 

class ProductoCreate(ProductoBase): #Esquema de alta de productos (cliente)
    pass #Hereda todos los campos de ProductoBase

class ProductoUpdate(BaseModel): #Modificacion, todos opcionales
    nombre: optional[str] = None
    precio: optional[float] = None
    id: optional[int] = None 

class ProductoResponse(ProductoBase): #Api response
    id: int 

class VentaBase(BaseModel): 
    id: int
    fecha: date  
    hora: time
    id_producto: int 
    cantidad: int
    precio_total: float 

class VentaCreate(VentaBase):
    pass

class VentaUpdate(BaseModel): 




class Config:
    from_atributes = True
    orm_mode = True #Pydantic lee SQL 