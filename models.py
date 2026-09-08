from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base 

class producto(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(50), nullable=False) 
    precio = Column(Float, nullable=False)

