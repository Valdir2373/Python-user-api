from abc import ABC, abstractmethod
from typing import Any, List

class IDataAccess(ABC):
    @abstractmethod
    async def testConnection(self, uri: str) -> bool:
        pass
    @abstractmethod
    async def dumpDatabase(self, uri: str, outputPath: str) -> None:
        pass
    @abstractmethod
    async def readTable(self, uri: str, tableName: str) -> List[Any]:
        pass
    @abstractmethod
    async def deleteRecord(self, uri: str, collection: str, filter: Any) -> bool:
        pass
    @abstractmethod
    async def find(self, uri: str, collection: str, query: Any) -> List[Any]:
        pass
    @abstractmethod
    async def insert(self, uri: str, collection: str, data: Any) -> Any:
        pass