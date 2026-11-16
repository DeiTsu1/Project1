from project1.models import Pet, User


class UserRepository:
    def __init__(self):
        self.__last__id = 0
        self.__table = dict[int, User]()

    async def save(self,user: User):
        self.__last__id += 1
        user.id = self.__last__id
        self.__table[user.id] = user
    
    async def get_by_id(self, id: int) -> User|None :
        return self.__table.get(id)
    
    async def get_all(self) -> list[User]:
        return list(self.__table.values())

class PetRepository:
    def __init__(self):
        self._pets: dict[int, Pet] = {}

    async def save(self, pet: Pet) -> Pet:
        self._pets[pet.id] = pet
        return pet

    async def get_all(self) -> list[Pet]:
        return list(self._pets.values())

    async def get_by_id(self, pet_id: int) -> Pet | None:
        return self._pets.get(pet_id)