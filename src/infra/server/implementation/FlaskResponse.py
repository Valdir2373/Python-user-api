from typing import Any, Optional, Dict
from flask import jsonify, make_response as flask_make_response, redirect as flask_redirect
from src.infra.server.interfaces.ICookieOptions import ICookieOptions


class FlaskResponse:
    def __init__(self, flask_req):
        self.flask_request = flask_req
        self.status_code = 200
        self.response_data = None
        self.headers_dict = {}

    def status(self, code: int) -> 'FlaskResponse':
        self.status_code = code
        return self

    def json(self, data: Any) -> None:
        self.response_data = jsonify(data)
        self._apply_status_and_headers()

    def send(self, data: Any) -> None:
        if isinstance(data, dict):
            self.json(data)
        else:
            self._send_text(data)

    def sendArchive(self, data: Any) -> None:
        self.response_data = flask_make_response(data, self.status_code)
        self._apply_headers()

    def setHeader(self, name: str, value: str) -> 'FlaskResponse':
        self.headers_dict[name] = value
        return self

    def cookie(self, name: str, value: str, options: Optional[ICookieOptions] = None) -> 'FlaskResponse':
        self._ensure_response_exists()
        cookie_kwargs = self._build_cookie_kwargs(options)
        self.response_data.set_cookie(name, value, **cookie_kwargs)
        return self

    def clearCookie(self, name: str, options: Optional[ICookieOptions] = None) -> 'FlaskResponse':
        self._ensure_response_exists()
        path = (options.path if options and options.path else "/")
        self.response_data.delete_cookie(name, path=path)
        return self

    def redirect(self, url: str) -> None:
        self.response_data = flask_redirect(url, code=self.status_code)

    def _send_text(self, data: Any) -> None:
        self.response_data = flask_make_response(str(data), self.status_code)
        self._apply_headers()

    def _ensure_response_exists(self) -> None:
        if self.response_data is None:
            self.response_data = flask_make_response("", self.status_code)

    def _apply_status_and_headers(self) -> None:
        self.response_data.status_code = self.status_code
        self._apply_headers()

    def _apply_headers(self) -> None:
        for key, value in self.headers_dict.items():
            self.response_data.headers[key] = value

    def _build_cookie_kwargs(self, options: Optional[ICookieOptions]) -> Dict[str, Any]:
        if options is None:
            options = ICookieOptions()
        
        kwargs = {
            'path': options.path or '/',
            'httponly': options.httpOnly if options.httpOnly is not None else True,
            'secure': options.secure if options.secure is not None else True,
            'samesite': options.sameSite if options.sameSite else 'lax'
        }
        
        self._add_optional_cookie_params(kwargs, options)
        return kwargs

    def _add_optional_cookie_params(self, kwargs: Dict[str, Any], options: ICookieOptions) -> None:
        if options.maxAge:
            kwargs['max_age'] = options.maxAge
        if options.expires:
            kwargs['expires'] = options.expires
        if options.domain:
            kwargs['domain'] = options.domain
