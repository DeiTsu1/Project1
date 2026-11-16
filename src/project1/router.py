import random
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status, HTTPException

from project1.models import UserRoll
from project1.schemas import (
    Pet,
    PetCreate,
    PetResponse,
    StatusResponse,
    User,
    UserCreate,
    UserResponse,
)
from project1.services import PetService, UserService

users_database: dict[int, User] = {}
pet_database: dict[int, Pet] = {}


router = APIRouter()

def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service


def get_pet_service(request: Request) -> PetService:
    return request.app.state.pet_service

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PetServiceDep = Annotated[PetService, Depends(get_pet_service)]

@router.get("/status")
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, user_service: UserServiceDep):
    for existing in users_database.values():
        if existing.login == user.login:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким логином уже существует",
            )
        if existing.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует",
            )

    await user_service.signup(user)

    user_id = random.randint(10_000_000, 99_999_999)
    while user_id in users_database:
        user_id = random.randint(10_000_000, 99_999_999)

    new_user = User(
        id=user_id,
        name=user.name,
        roll=UserRoll.USER,
        login=user.login,
        email=user.email,
        password=user.password,
    )
    users_database[user_id] = new_user

    return UserResponse(
    id=new_user.id,
    name=new_user.name,
    roll=new_user.roll,
    login=new_user.login,
    email=new_user.email,
)

@router.get("/users", response_model=list[UserResponse])
def list_users() -> list[UserResponse]:
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            roll=user.roll,
            login=user.login,
            email=user.email,
        )
        for user in users_database.values()
    ]

@router.get("/users/{id}", response_model=UserResponse)
async def get_user_by_id(id: int) -> UserResponse:
    user = users_database.get(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return UserResponse(id=user.id, name=user.name, email=user.email)


#ДЗ
@router.post("/pets", status_code=status.HTTP_201_CREATED, response_model=PetResponse)
async def create_pet(pet: PetCreate, pet_service: PetServiceDep) -> PetResponse:
    new_pet = await pet_service.create(pet)
    return PetResponse(**new_pet.model_dump())


@router.get("/pets", response_model=list[PetResponse])
async def list_pets(pet_service: PetServiceDep) -> list[PetResponse]:
    return [PetResponse(**p.model_dump()) for p in await pet_service.get_all()]
    
