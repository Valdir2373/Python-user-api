from typing import Any, Dict, Optional


class FlaskRequest:
    def __init__(self, flask_req, route_params: Dict[str, Any] = None):
        self.flask_request = flask_req
        self.body = flask_req.get_json(silent=True) or {}
        self.params = self._merge_params(dict(flask_req.args), route_params)
        self.query = dict(flask_req.args)
        self.headers = dict(flask_req.headers)
        self.method = flask_req.method
        self.path = flask_req.path
        self.userPayload = None
        self.cookies = dict(flask_req.cookies)

    def _merge_params(self, query_params: Dict[str, Any], route_params: Dict[str, Any] = None) -> Dict[str, Any]:
        if route_params is None:
            return query_params
        return {**query_params, **route_params}
