import random

from fastapi import status
from fastapi.exceptions import HTTPException

from project1.models import Pet, PetCreate, User, UserRoll
from project1.repositories import PetRepository, UserRepository
from project1.schemas import UserCreate

class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def signup(self, user: UserCreate) -> User:
        all_users = await self._user_repository.get_all()
        if len(all_users) == 0:
            roll = UserRoll.ADMIN
        else:
            roll = UserRoll.USER

        model = User(
            id=0,
            name=user.name,
            roll=roll,
            login=user.login,
            email=user.email,
            password=user.password,
        )
        await self._user_repository.save(model)
        return model

    async def get_by_id(self, id: int) -> User | None:
        model = await self._user_repository.get_by_id(id)
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User was not found",
            )
        return model

    async def get_all(self) -> list[User]:
        return await self._user_repository.get_all()

VID_LIST = ["собакен", "попугай", "утконос", "котэ", "лошадка", "что-то", "черепахен", "женщина"]

class PetService:
    def __init__(self, pet_repository: PetRepository):
        self._pet_repository = pet_repository

    async def create(self, pet: PetCreate) -> Pet:
        vid = random.choice(VID_LIST)
        pet_id = random.randint(10_000_000, 99_999_999)
        while await self._pet_repository.get_by_id(pet_id) is not None:
            pet_id = random.randint(10_000_000, 99_999_999)

        model = Pet(id=pet_id, name=pet.name, vid=vid)
        await self._pet_repository.save(model)
        return model

    async def get_all(self) -> list[Pet]:
        return await self._pet_repository.get_all()