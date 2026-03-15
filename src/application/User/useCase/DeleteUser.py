from src.domain.repository.IUserRepository import IUserRepository


class DeleteUser:
    def __init__(self, userRepo: IUserRepository):
        self.userRepo = userRepo

    async def Execute(self, userId: str) -> bool:
        user = await self.userRepo.GetById(userId)
        if not user:
            raise Exception("User not found")
        return await self.userRepo.Delete(userId)