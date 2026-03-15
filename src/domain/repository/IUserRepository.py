from abc import ABC, abstractmethod
from typing import Optional
from ..entities.User import User

class IUserRepository(ABC):

    @abstractmethod
    async def Save(self, user: User) -> None:
        pass

    @abstractmethod
    async def GetByEmail(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def GetById(self, userId: str) -> Optional[User]:
        pass

    @abstractmethod
    async def Delete(self, userId: str) -> bool:
        pass