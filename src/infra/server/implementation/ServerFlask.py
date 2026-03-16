from typing import Any, Callable, Optional, Dict
from flask import Flask, request as flask_request
from src.infra.server.interfaces.IServer import IServer
from src.infra.server.interfaces.IMiddlewareHandler import MiddlewareHandler
from src.infra.server.implementation.FlaskRequest import FlaskRequest
from src.infra.server.implementation.FlaskResponse import FlaskResponse
import asyncio


class ServerFlask(IServer):
    def __init__(self, app_name: str = "API"):
        self.app = Flask(app_name)
        self.routes = {}

    def registerRouter(
        self, 
        methodHTTP: str, 
        path: str, 
        *handlers: MiddlewareHandler
    ) -> None:
        def route_handler(**kwargs):
            req = FlaskRequest(flask_request, route_params=kwargs)
            res = FlaskResponse(flask_request)
            asyncio.run(self._execute_middleware_chain(handlers, req, res))
            return res.response_data or ("", res.status_code)
        
        self._register_route(methodHTTP, path, route_handler)

    def listen(self, port: int, callback: Optional[Callable[[], None]] = None) -> Any:
        if callback:
            callback()
        self.app.run(host="0.0.0.0", port=port, debug=False)
        return self.app

    def getHttpServer(self) -> Any:
        return self.app

    async def _execute_middleware_chain(self, handlers: tuple, req: FlaskRequest, res: FlaskResponse) -> None:
        handler_index = 0
        
        async def next_handler():
            nonlocal handler_index
            if handler_index < len(handlers):
                current = handlers[handler_index]
                handler_index += 1
                await current(req, res, next_handler)
        
        await next_handler()

    def _register_route(self, methodHTTP: str, path: str, handler: Callable) -> None:
        route_key = f"{methodHTTP.upper()}:{path}"
        self.routes[route_key] = handler
        self.app.add_url_rule(
            path,
            f"{methodHTTP.upper()}_{path.replace('/', '_')}",
            handler,
            methods=[methodHTTP.upper()]
        )
