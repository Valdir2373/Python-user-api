from dataclasses import dataclass

@dataclass
class UserInput:
    username: str
    email: str
    password: str