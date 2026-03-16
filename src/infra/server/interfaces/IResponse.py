from abc import ABC, abstractmethod
from typing import Any, Optional
from .ICookieOptions import ICookieOptions


class IResponse(ABC):
    @abstractmethod
    def status(self, code: int) -> 'IResponse':
        pass

    @abstractmethod
    def json(self, data: Any) -> None:
        pass

    @abstractmethod
    def send(self, data: Any) -> None:
        pass

    @abstractmethod
    def sendArchive(self, data: Any) -> None:
        pass

    @abstractmethod
    def setHeader(self, name: str, value: str) -> 'IResponse':
        pass

    @abstractmethod
    def cookie(self, name: str, value: str, options: Optional[ICookieOptions] = None) -> 'IResponse':
        pass

    @abstractmethod
    def clearCookie(self, name: str, options: Optional[ICookieOptions] = None) -> 'IResponse':
        pass

    @abstractmethod
    def redirect(self, url: str) -> None:
        pass
