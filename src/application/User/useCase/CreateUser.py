from src.domain.entities.User import User
from src.domain.repository.IUserRepository import IUserRepository
from src.application.User.dtos.UserInput import UserInput
from src.application.User.dtos.UserOutput import UserOutput
from typing import Callable

class CreateUser:
    def __init__(self, userRepo: IUserRepository):
        self.userRepo = userRepo

    async def Execute(self, userInput: UserInput, createId: Callable[[], str]) -> UserOutput:
        userExists = await self.userRepo.GetByEmail(userInput.email)
        if userExists:
            raise Exception("Email already in use")

        newUser = User.Build(userInput.username, userInput.email, userInput.password, createId)
        await self.userRepo.Save(newUser)
        return UserOutput(id=newUser.id, username=newUser.username, email=newUser.email)