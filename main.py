from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Owner, Dog  # Asegúrate de que estos modelos están en `database.py`
from pydantic import BaseModel, EmailStr, constr
from datetime import date

app = FastAPI()

# Crear un cliente de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic para validación
class OwnerCreate(BaseModel):
    nombre: constr(min_length=1, max_length=50)
    apellidos: constr(min_length=1, max_length=50)
    ciudad: constr(min_length=1, max_length=50)
    postalcode: int
    email: EmailStr
    telefono: constr(min_length=9, max_length=15)
class DogCreate(BaseModel):
    nombre_perro: constr(min_length=1, max_length=50)
    fecha_nacimiento: str  # Puedes usar `datetime.date` si prefieres
    peso: float
    id_dueño: int
    sexo: str  # 'macho' o 'hembra'
    esterilizado: bool


# Crear un nuevo dueño
@app.post("/owners/")
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    db_owner = Owner(**owner.dict())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

# Crear un nuevo perro
@app.post("/dogs/")
def create_dog(dog: DogCreate, db: Session = Depends(get_db)):
    # Verificar que el dueño existe
    db_owner = db.query(Owner).filter(Owner.id == dog.owner_id).first()
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    db_dog = Dog(**dog.dict())
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog

# Obtener todos los dueños
@app.get("/owners/")
def read_owners(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    owners = db.query(Owner).offset(skip).limit(limit).all()
    return owners

# Obtener todos los perros
@app.get("/dogs/")
def read_dogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dogs = db.query(Dog).offset(skip).limit(limit).all()
    return dogs

# Obtener un dueño por ID
@app.get("/owners/{owner_id}")
def read_owner(owner_id: int, db: Session = Depends(get_db)):
    db_owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return db_owner

# Obtener un perro por ID
@app.get("/dogs/{dog_id}")
def read_dog(dog_id: int, db: Session = Depends(get_db)):
    db_dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return db_dog

# Actualizar un dueño
@app.put("/owners/{owner_id}")
def update_owner(owner_id: int, owner: OwnerCreate, db: Session = Depends(get_db)):
    db_owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    for key, value in owner.dict().items():
        setattr(db_owner, key, value)
    
    db.commit()
    return db_owner

# Actualizar un perro
@app.put("/dogs/{dog_id}")
def update_dog(dog_id: int, dog: DogCreate, db: Session = Depends(get_db)):
    db_dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    for key, value in dog.dict().items():
        setattr(db_dog, key, value)
    
    db.commit()
    return db_dog

# Eliminar un dueño
@app.delete("/owners/{owner_id}")
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    db_owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    db.delete(db_owner)
    db.commit()
    return {"detail": "Owner deleted"}

# Eliminar un perro
@app.delete("/dogs/{dog_id}")
def delete_dog(dog_id: int, db: Session = Depends(get_db)):
    db_dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    db.delete(db_dog)
    db.commit()
    return {"detail": "Dog deleted"}

@app.get("/dogs/city/{city_name}")
def get_dogs_by_city(city_name: str, db: Session = Depends(get_db)):
    # Hacer un JOIN entre Dog y Owner para buscar perros por ciudad
    dogs = db.query(Dog).join(Owner).filter(Owner.ciudad == city_name).all()
    return dogs

@app.get("/dogs/owner-name/{owner_name}/{owner_surname}")
def get_dogs_by_owner_name_and_surname(owner_name: str, owner_surname: str, db: Session = Depends(get_db)):
    dogs = db.query(Dog).join(Owner).filter(Owner.nombre == owner_name, Owner.apellidos == owner_surname).all()
    return dogs

@app.get("/dogs/sex/{sex}")
def get_dogs_by_sex(sex: str, db: Session = Depends(get_db)):
    dogs = db.query(Dog).filter(Dog.sexo == sex).all()
    return dogs

@app.get("/dogs/sterilized/{is_sterilized}")
def get_dogs_by_sterilization(is_sterilized: bool, db: Session = Depends(get_db)):
    dogs = db.query(Dog).filter(Dog.esterilizado == is_sterilized).all()
    return dogs
