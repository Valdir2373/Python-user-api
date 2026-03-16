from typing import Callable, Any, Coroutine
from .IRequest import IRequest
from .IResponse import IResponse


MiddlewareHandler = Callable[
    [IRequest, IResponse, Callable[[], Coroutine[Any, Any, None]]], 
    Coroutine[Any, Any, None]
]
