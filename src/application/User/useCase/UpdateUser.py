from src.domain.repository.IUserRepository import IUserRepository
from src.application.User.dtos.UserInput import UserInput
from src.application.User.dtos.UserOutput import UserOutput
from src.domain.entities.User import User

class UpdateUser:
    def __init__(self, userRepo: IUserRepository):
        self.userRepo = userRepo

    async def Execute(self, userId: str, userInput: UserInput) -> UserOutput:
        user = await self.userRepo.GetById(userId)
        if not user:
            raise Exception("User not found")
        
        user.username = userInput.username
        user.email = userInput.email
        user.passwordHash = userInput.password
        
        await self.userRepo.Save(user)
        return UserOutput(id=user.id, username=user.username, email=user.email)