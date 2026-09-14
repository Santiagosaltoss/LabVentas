from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from database import Base 
from sqlalchemy.sql import func

class Producto(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(50), nullable=False) 
    precio = Column(Float, nullable=False)

class Ventas(Base):
    __tablename__ = 'ventas'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

