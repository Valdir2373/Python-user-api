from dataclasses import dataclass

@dataclass
class UserLoginInput:
    email: str
    password: str