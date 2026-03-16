from dataclasses import dataclass
from typing import Optional, Callable, Literal, Union
from datetime import datetime


@dataclass
class ICookieOptions:
    domain: Optional[str] = None
    encode: Optional[Callable[[str], str]] = None
    expires: Optional[datetime] = None
    httpOnly: Optional[bool] = True
    maxAge: Optional[int] = None
    path: Optional[str] = "/"
    priority: Optional[Literal["low", "medium", "high"]] = None
    secure: Optional[bool] = True
    signed: Optional[bool] = None
    sameSite: Optional[Union[Literal["strict", "lax", "none"], bool]] = "lax"
