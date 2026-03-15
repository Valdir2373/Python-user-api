from dataclasses import dataclass
from datetime import datetime
from typing import Callable

@dataclass
class User:
    id: str
    username: str
    email: str
    passwordHash: str
    createdAt: datetime

    @staticmethod
    def Build(username: str, email: str, passwordHash: str, createId: Callable[[], str]) -> User:
        return User(
            id=createId(),
            username=username,
            email=email,
            passwordHash=passwordHash,
            createdAt=datetime.now()
        )