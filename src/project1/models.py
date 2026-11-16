from enum import StrEnum

from pydantic import BaseModel


class UserRoll(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(BaseModel):
    id: int
    name: str
    roll: UserRoll
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