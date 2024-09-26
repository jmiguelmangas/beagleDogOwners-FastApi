from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Crear una base declarativa
Base = declarative_base()

# Modelo para Owners
class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    postalcode = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=False)

# Modelo para Dogs
class Dog(Base):
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    peso = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    sexo = Column(String, nullable=False)
    esterilizado = Column(Boolean, nullable=False)

# Configurar la conexión a la base de datos (aquí se utiliza SQLite)
engine = create_engine('sqlite:///mydatabase.db')  # Cambia a tu base de datos si es necesario
Base.metadata.create_all(engine)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
