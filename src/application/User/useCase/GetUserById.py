from src.domain.repository.IUserRepository import IUserRepository
from src.application.User.dtos.UserOutput import UserOutput

class GetUserById:
    def __init__(self, userRepo: IUserRepository):
        self.userRepo = userRepo

    async def Execute(self, userId: str) -> UserOutput:
        user = await self.userRepo.GetById(userId)
        if not user:
            raise Exception("User not found")
        return UserOutput(id=user.id, username=user.username, email=user.email)