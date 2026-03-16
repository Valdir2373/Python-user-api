from typing import Any, Dict, Optional
from src.infra.server.interfaces.IRequest import IRequest


class FlaskRequest(IRequest):
    def __init__(self, flask_request):
        self.flask_request = flask_request
        self.body = flask_request.get_json(silent=True) or {}
        self.params = dict(flask_request.args)
        self.query = dict(flask_request.args)
        self.headers = dict(flask_request.headers)
        self.method = flask_request.method
        self.path = flask_request.path
        self.userPayload = None
        self.cookies = dict(flask_request.cookies)
