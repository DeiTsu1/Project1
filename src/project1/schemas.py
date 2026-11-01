from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str

class UserResponse(BaseModel):
    name: str
    email: str

class User(BaseModel):
    name: str
    login: str
    email: str
    password: str

class Pet(BaseModel):
    id: int
    name: str
    vid: str

class PetCreate(BaseModel):
    name: str
    vid: str

class PetResponse(BaseModel):
    id: int
    name: str
    vid: str
