from typing import Any, Callable, Optional
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
        def route_handler():
            req = FlaskRequest(flask_request)
            res = FlaskResponse(flask_request)
            
            async def execute_handlers():
                handler_index = 0
                
                async def next_handler():
                    nonlocal handler_index
                    if handler_index < len(handlers):
                        current = handlers[handler_index]
                        handler_index += 1
                        await current(req, res, next_handler)
                
                await next_handler()
            
            asyncio.run(execute_handlers())
            
            return res.response_data or ("", res.status_code)
        
        route_key = f"{methodHTTP.upper()}:{path}"
        self.routes[route_key] = route_handler
        
        methods = [methodHTTP.upper()]
        self.app.add_url_rule(
            path, 
            f"{methodHTTP.upper()}_{path.replace('/', '_')}", 
            route_handler, 
            methods=methods
        )

    def listen(self, port: int, callback: Optional[Callable[[], None]] = None) -> Any:
        if callback:
            callback()
        
        self.app.run(host="0.0.0.0", port=port, debug=False)
        return self.app

    def getHttpServer(self) -> Any:
        return self.app
