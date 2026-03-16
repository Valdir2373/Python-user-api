from typing import Any, Dict, Optional


class IRequest:
    body: Any
    params: Dict[str, Any]
    query: Dict[str, Any]
    headers: Dict[str, Any]
    method: str
    path: str
    userPayload: Optional[Any] = None
    cookies: Optional[Dict[str, str]] = None
