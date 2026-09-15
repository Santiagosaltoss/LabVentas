from pydantic import BaseModel
from typing import Optional 
from datetime import datetime

class ProductoBase(BaseModel): #Base comun para todos los campos
    nombre: str
    precio: float 

class ProductoCreate(ProductoBase): #Esquema de alta de productos (cliente)
    pass #Hereda todos los campos de ProductoBase

class ProductoUpdate(BaseModel): #Modificacion, todos opcionales
    nombre: optional[str] = None
    precio: optional[float] = None

class ProductoResponse(ProductoBase): #Api response
    id: int 

class VentaBase(BaseModel):
    id_producto: int
    cantidad: int
    


class VentaCreate(VentaBase):
    pass 

# 3. Esquema para Actualizar 
class VentaUpdate(BaseModel):
    id_producto: Optional[int] = None
    cantidad: Optional[int] = None
    precio_total: Optional[float] = None

# 4. (Lo que la API DEVUELVE al cliente)
class VentaResponse(VentaBase):
    id: int
    precio_total: float              
    fecha: datetime       

    model_config = {"from_attributes": True}



class Config:
    from_atributes = True
    orm_mode = True #Pydantic lee SQL 