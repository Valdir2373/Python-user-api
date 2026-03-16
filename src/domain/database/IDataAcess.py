from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar, Generic, Dict, Sequence, Union

T = TypeVar("T")

class IDataAccess(ABC):
    @abstractmethod
    async def find_many(
        self, 
        collection_name: str, 
        query: Optional[Dict[str, Any]] = None, 
        select_fields: Optional[Sequence[str]] = None
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def find_one(
        self, 
        collection_name: str, 
        query: Dict[str, Any], 
        select_fields: Optional[Sequence[str]] = None
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def create(
        self, 
        collection_name: str, 
        data: Dict[str, Any]
    ) -> Union[str, int, None]:
        pass

    @abstractmethod
    async def update(
        self, 
        collection_name: str, 
        query: Dict[str, Any], 
        data: Dict[str, Any]
    ) -> int:
        pass

    @abstractmethod
    async def remove(
        self, 
        collection_name: str, 
        query: Dict[str, Any]
    ) -> int:
        pass