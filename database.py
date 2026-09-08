from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./mi_base_de_datos.db"

# Motor que administra las conexiones
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Requerido solo para SQLite
)

# Fábrica de sesiones para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán nuestros modelos
Base = declarative_base()

# Generador para obtener la sesión en cada operación
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()