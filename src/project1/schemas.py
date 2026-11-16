from typing import Annotated
from enum import StrEnum

from pydantic import BaseModel, EmailStr, StringConstraints



class StatusResponse(BaseModel):
    status: str

class UserRoll(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserResponse(BaseModel):
    id: int
    name: str
    roll: UserRoll
    login: str
    email: EmailStr


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


class UserCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]
    login: Annotated[str, StringConstraints(min_length=1)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=6, max_length=32)]
