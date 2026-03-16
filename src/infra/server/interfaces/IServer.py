from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from .IMiddlewareHandler import MiddlewareHandler


class IServer(ABC):
    @abstractmethod
    def registerRouter(
        self, 
        methodHTTP: str, 
        path: str, 
        *handlers: MiddlewareHandler
    ) -> None:
        pass

    @abstractmethod
    def listen(self, port: int, callback: Optional[Callable[[], None]] = None) -> Any:
        pass

    @abstractmethod
    def getHttpServer(self) -> Any:
        pass
