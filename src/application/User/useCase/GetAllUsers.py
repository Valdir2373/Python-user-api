from src.domain.repository.IUserRepository import IUserRepository
from src.application.User.dtos.UserOutput import UserOutput
from typing import List

class GetAllUsers:
    def __init__(self, userRepo: IUserRepository):
        self.userRepo = userRepo

    async def Execute(self) -> List[UserOutput]:
        users = await self.userRepo.GetAll()
        return [UserOutput(id=user.id, username=user.username, email=user.email) for user in users]