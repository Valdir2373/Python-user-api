from dataclasses import dataclass

@dataclass
class UserOutput:
    id: str
    username: str
    email: str