from fastapi import FastAPI

from project1.repositories import PetRepository, UserRepository
from project1.router import router
from project1.services import PetService, UserService

app = FastAPI()

user_repository = UserRepository()
app.state.user_service = UserService(user_repository)

pet_repository = PetRepository()
app.state.pet_service = PetService(pet_repository)

app.include_router(router)