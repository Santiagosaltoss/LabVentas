# crud.py
from sqlalchemy.orm import Session
import models, schemas

# 1. LEER (Read / Consulta)
def obtener_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

# 2. CREAR (Create / Alta)
def crear_producto(db: Session, producto: schemas.ProductoCreate):
    # Convertimos el esquema de Pydantic a un modelo ORM de SQLAlchemy
    db_producto = models.Producto(
        nombre=producto.nombre,
        id=producto.id,
        precio=producto.precio,
    )
    db.add(db_producto)       # Se agrega a la transacción
    db.commit()               # Se aplican los cambios en la DB
    db.refresh(db_producto)   # Carga el ID asignado automáticamente
    return db_producto

# 3. ACTUALIZAR (Update / Modificación)
def actualizar_producto(db: Session, producto_id: int, producto_data: schemas.ProductoCreate):
    db_producto = obtener_producto(db, producto_id)
    if not db_producto:
        return None
    
    # Sobreescribe todos los atributos con los nuevos valores recibidos
    db_producto.nombre = producto_data.nombre
    db_producto.precio = producto_data.precio
    db_producto.id = producto_data.id 
        
    db.commit()
    db.refresh(db_producto)
    return db_producto

# 4. ELIMINAR (Delete / Baja)
def eliminar_producto(db: Session, producto_id: int):
    db_producto = obtener_producto(db, producto_id)
    if not db_producto:
        return False
    
    db.delete(db_producto) # Marca para eliminación
    db.commit()            # Confirma la eliminación
    return True


def obtener_venta(db: Session, venta_id: int):
    return db.query(models.Ventas).filter(models.Ventas.id == ventas.id).first()

def obtener_ventas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ventas).offset(skip).limit(limit).all()

def crear_venta(db: Session, producto: schemas.VentaCreate):
    # Convertimos el esquema de Pydantic a un modelo ORM de SQLAlchemy
    db_venta = models.Ventas(
        id_producto=producto.id,
        cantidad=venta.cantidad,
        precio_total=venta.precio_total,
    )
    db.add(db_producto)       # Se agrega a la transacción
    db.commit()               # Se aplican los cambios en la DB
    db.refresh(db_producto)   # Carga el ID asignado automáticamente
    return db_producto

def actualizar_venta(db: Session, venta_id: int, venta_data: schemas.VentaCreate):
    db_venta = obtener_venta(db, venta_id)
    if not db_venta:
        return None
    
    # Sobreescribe todos los atributos con los nuevos valores recibidos
    db_venta.id_producto = venta_data.id_producto
    db_venta.cantidad = venta_data.cantidad
    db_venta.precio_total = venta_data.precio_total
        
    db.commit()
    db.refresh(db_producto)
    return db_venta

def eliminar_venta(db: Session, venta_id: int) -> bool:
    db_venta = obtener_venta(db, venta_id)
    if not db_venta:
        return False
    
    db.delete(db_venta)
    db.commit()
    return True   


