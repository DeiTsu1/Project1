import random

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from project1.schemas import (
    Pet,
    PetCreate,
    PetResponse,
    StatusResponse,
    User,
    UserResponse,
)

router = APIRouter()

users_database: dict[str, User]() = {}
pet_database: dict[int, Pet]() = {}

VID_LIST = ["собакен","попугай", "утконос", "котэ", "лошадка", "что-то", "черепахен", "женщина"]

@router.get("/status")
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user:User):
    global users_database
    if user.login in users_database:
        raise HTTPException(status.HTTP_409_CONFLICT)
    users_database[user.login] = user

@router.get("/users/{login}")
def get_user(login:str) -> UserResponse:
    if login not in users_database:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    user = users_database[login]
    return UserResponse(name = user.name,email = user.email)
    

#ДЗ
@router.post("/pets",status_code=status.HTTP_201_CREATED, response_model= PetResponse)
def create_pet(pet: PetCreate):
    vid = random.choice(VID_LIST)
    pet_id = random.randint(10_000_000,99_999_999)
    while pet_id in pet_database:
        pet_id = random.randint(10_000_000, 99_999_999)
    new_pet = Pet(id = pet_id, name = pet.name, vid = vid)
    pet_database[pet_id] = new_pet

    return PetResponse(id= new_pet.id, name= new_pet.name, vid= new_pet.vid)

@router.get("/pets", response_model= list[PetResponse])
def list_pets() -> list[PetResponse]:
    return [PetResponse(id= p.id, name= p.name, vid= p.vid) for p in pet_database.values()]
    
