from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, UserModel


app = FastAPI()

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str


class UserUpdate(BaseModel):
    name: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserModel(name=user.name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.put("/users/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .first()
    )

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user.name

    db.commit()
    db.refresh(existing_user)

    return existing_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .first()
    )

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(existing_user)
    db.commit()

    return {"message": "user deleted successfully"}
