from typing import Any, Optional
from flask import jsonify, make_response as flask_make_response, redirect as flask_redirect
from src.infra.server.interfaces.IResponse import IResponse
from src.infra.server.interfaces.ICookieOptions import ICookieOptions
import json


class FlaskResponse(IResponse):
    def __init__(self, flask_response):
        self.flask_response = flask_response
        self.status_code = 200
        self.response_data = None
        self.headers_dict = {}

    def status(self, code: int) -> 'FlaskResponse':
        self.status_code = code
        return self

    def json(self, data: Any) -> None:
        self.response_data = jsonify(data)
        self.response_data.status_code = self.status_code
        for key, value in self.headers_dict.items():
            self.response_data.headers[key] = value

    def send(self, data: Any) -> None:
        if isinstance(data, dict):
            self.json(data)
        else:
            self.response_data = flask_make_response(str(data), self.status_code)
            for key, value in self.headers_dict.items():
                self.response_data.headers[key] = value

    def sendArchive(self, data: Any) -> None:
        self.response_data = flask_make_response(data, self.status_code)
        for key, value in self.headers_dict.items():
            self.response_data.headers[key] = value

    def setHeader(self, name: str, value: str) -> 'FlaskResponse':
        self.headers_dict[name] = value
        return self

    def cookie(self, name: str, value: str, options: Optional[ICookieOptions] = None) -> 'FlaskResponse':
        if self.response_data is None:
            self.response_data = flask_make_response("", self.status_code)
        
        if options is None:
            options = ICookieOptions()
        
        kwargs = {
            'path': options.path or '/',
            'httponly': options.httpOnly if options.httpOnly is not None else True,
            'secure': options.secure if options.secure is not None else True,
            'samesite': options.sameSite if options.sameSite else 'lax'
        }
        
        if options.maxAge:
            kwargs['max_age'] = options.maxAge
        if options.expires:
            kwargs['expires'] = options.expires
        if options.domain:
            kwargs['domain'] = options.domain
        
        self.response_data.set_cookie(name, value, **kwargs)
        return self

    def clearCookie(self, name: str, options: Optional[ICookieOptions] = None) -> 'FlaskResponse':
        if self.response_data is None:
            self.response_data = flask_make_response("", self.status_code)
        
        if options is None:
            options = ICookieOptions()
        
        kwargs = {
            'path': options.path or '/',
        }
        
        self.response_data.delete_cookie(name, **kwargs)
        return self

    def redirect(self, url: str) -> None:
        self.response_data = flask_redirect(url, code=self.status_code)
