from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class UserCreate(BaseModel):
    name: str


class UserUpdate(BaseModel):
    name: str


app = FastAPI()

# Shared users list
users = [
    User(id=1, name="Alice"),
    User(id=2, name="Bob"),
    User(id=3, name="Charlie")
]


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/users")
def get_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_id = len(users) + 1
    new_user = User(id=new_id, name=user.name)
    users.append(new_user)
    return new_user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate):
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.name = user.name
            return existing_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for existing_user in users:
        if existing_user.id == user_id:
            users.remove(existing_user)
            return {"message": "user deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
