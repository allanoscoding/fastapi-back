from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entidad User


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Angel", surname="Llanos", url="https://moure.dev", age=21),
              User(id=2, name="Moure", surname="Dev", url="https://moure.dev", age=35),
              User(id=3, name="Oscar", surname="Ortega", url="https://moure.dev", age=22)]


@app.get("/usersjson")
async def users_json():
    return [{"name": "Angel", "surname": "Llanos", "url": "https://moure.dev", "age": 21},
            {"name": "Brais", "surname": "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Oscar", "surname": "Ortega", "url": "https://moure.dev", "age": 22}]


@app.get("/users")
async def users():
    return users_list


# Path
@app.get("/user/{id}")
async def user(id: int):
    return search_users(id)


# Query
@app.get("/user/")
async def user(id: int):
    return search_users(id)


@app.post("/user/")
async def user(user: User):
    if type(search_users(user.id)) == User:
        return {"error": "El usuario ya existe en la DB"}

    users_list.append(user)
    return user


@app.put("/user/")
async def user(user: User):

    found = False

    for idx, saved_users in enumerate(users_list):
        if saved_users.id == user.id:
            users_list[idx] = user

    if not found:
        return {"error": "El usuario no existe en la DB"}

    return user


@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for idx, saved_users in enumerate(users_list):
        if saved_users.id == id:
            del users_list[idx]
            found = True

    if not found:
        return {"error": "El usuario ya existe en la DB"}


def search_users(id: int):
    found_users = filter(lambda user: user.id == id, users_list)
    try:
        return list(found_users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}




